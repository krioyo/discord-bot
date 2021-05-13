#github was here 2

import asyncio
import csv
import discord
import json
import time
import sys
import os
#import colorama
from datetime import datetime
from errors import checkerrors
from discord.ext import commands
import errors

with open("settings.json") as settings:
    data = json.load(settings)


client = discord.Client()
cd = "./files/"
ganesh = "Ganesh_template.csv"
timestamp = datetime.now().strftime("[%H:%M:%S] ")

questions = [("AMOUNT", "How many pairs would you want?\n\nPlease input a number\nExample: **8**"),
             ("FIRST NAME","What is your first name?\n\nPlease input only one word\nExample: **Josh**"),
             ("LAST NAME","What is your last name?\n\nPlease input only one word\nExample: **Smith**"),
             ("EMAIL","What is your email?\n\nPlease input a valid email\nExample: **test@gmail.com**"),
             ("PHONE NUMBER","What is your phone number?\n\nPlease input a valid number\nExample: **0683475291**"),
             ("ADDRESS LINE 1","Address line 1\n\nPlease input a number\nExample: **Sneakerstreet 13**"),
             ("ADDRESS LINE 2","Address line 2 (if needed) (type !skip if it is not needed)"),
             ("CITY","City\n\nPlease input the name of the city\nExample: **Snkrzone**"),
             ("STATE","State (if needed)\n\n(type !skip if it is not needed)\nExample:**Sneaker**"),
             ("POSTCODE / ZIP","Postal code\n\nPlease input in a right format\nExample: **33194**"),
             ("COUNTRY","Country\n\nPlease input the 2 letter abbreviation\nExamples: **NL/CZ/PT/PL**"),
             ("CARD NUMBER","Card number\n\nPlease input the card number in the following format\nExample: **1234123412341234**"),
             ("EXPIRE MONTH","Expiry month\n\nPlease input 2 numbers\nExample for May: **05**"),
             ("EXPIRE YEAR","Expiry year\n\nPlease input 4 numbers\nExample: **2025**"),
             ("CARD CVC","Card cvc\n\nPlease input the 3 numbers on the back of your card\nExample: **123**")]

user_check = ["Amount of pairs: ",
            "First name: ",
            "Last name: ",
            "Email: ",
            "Phone number: ",
            "Address line 1: ",
            "Address line 2: ",
            "City: ",
            "State: ",
            "Postal code: ",
            "Country: ",
            "Card number: ",
            "Expiry month: ",
            "Expiry year: ",
            "CVC: "]

user_amount = []

bot = commands.Bot(command_prefix='$')

@client.event
async def on_ready():
    print(timestamp + 'Logged in as {0.user}'.format(client))
    # Add function that counts amount of channels being monitored in a category and display in playing status
    status = len(client.get_channel(data['TICKETS_CATEGORY']).text_channels)
    whole = "Watching {} tickets".format(status)
    print(whole)
    # await client.change_presence(activity=discord.Activity(name=f"👀 Watching" + status + " tickets"))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing,name=whole))

# Takes header out of file to use in template
with open('{}{}'.format(cd,ganesh), 'r') as file:
    reader = csv.reader(file)
    header_ganesh = next(reader)

def currentTime():
    return datetime.now().strftime("[%H:%M:%S] ")

# async def getChannels():
#     cat == data['CATEGORY']
#     print(get(cat))

# @commands.command(name="konjo")
# async def _konjo(ctx,arg):
#     await message.channel.send(arg)
print(user_amount)
@client.event
async def on_message(message):
    author = message.author
    msg = message.content
    
    answers_keys = ["AMOUNT",
             "FIRST NAME",
             "LAST NAME",
             "EMAIL",
             "PHONE NUMBER",
             "ADDRESS LINE 1",
             "ADDRESS LINE 2",
             "CITY",
             "STATE",
             "POSTCODE / ZIP",
             "COUNTRY",
             "CARD NUMBER",
             "EXPIRE MONTH",
             "EXPIRE YEAR",
             "CARD CVC"]

    # Array of answers that the user sent in the channel
    answers = []
    

    if message.author == client.user:
        return

    if msg.startswith('!off'):
        if author.id in data['ADMINS']:
            sys.exit('Turned off by {}'.format(author))
        else:
            print("User {} tried using admin command".format(author))
            return

    if msg.startswith('!ganesh'):
        # logger = client.get_channel(835830723838607430)
        logger = client.get_channel(data['LOGGER'])
        await message.channel.send(file=discord.File(r'{}{}'.format(cd,ganesh))) # Add more bot templates
        await logger.send('Sent ganesh template to {}'.format(author))
        print('Sent ganesh template to', author)
        


 
    if message.content.startswith('!form'):
        i = 0
        n = 15 #len(questions) # Read amount of questions etc and have it as variable
                    
        def check(reply):
            return reply.author == message.author and reply.channel == message.channel

        try:
            #the start van de n vragen loop
            while i != n and i >= 0:
                print(currentTime() + u"\u001b[33mAsking {} question number {}...\u001b[0m".format(author,i+1))
                embed=discord.Embed(title="Question {}/{}".format(i+1,n),
                        description=questions[i][1],
                        color=0xFF5733)

                await message.channel.send(embed=embed)
                reply = await client.wait_for("message", check=check, timeout=120)

                if "!FORM" in reply.content.upper():
                    await message.channel.send("You restarted the form...")
                    answers=[]
                    i=0
                    continue
                
                if "!STOP" in reply.content.upper():
                    print(currentTime() + "Stopping the form for {}".format(author))
                    await message.channel.send("Closing the form...")
                    return

                if "!BACK" in reply.content.upper():
                    if i == 0:
                        await message.channel.send("You can't do that...")
                        continue
                    else:
                        await message.channel.send("Going back to the previous question...")
                        del answers[-1]
                        i -= 1
                        continue

                if "!RESTART" in reply.content.upper():
                    print(currentTime() + "Restarting the form for {}".format(author))
                    await message.channel.send("Restarting the form...")
                    answers = []
                    i = 0
                    continue
                
                if "!SKIP" in reply.content.upper():
                    print(currentTime() + "User skipped question")
                    answers.append("")
                    i+=1
                    continue

                if checkerrors(reply.content, questions[i][0]):
                    answers.append(reply.content)
                    if questions[i][0] == "AMOUNT":
                        user_amount.append((author, reply.content))
                    i += 1
                else:
                    await message.channel.send(errors.errormessage)
                
                

        except asyncio.TimeoutError:
            await message.channel.send("Sorry you did not reply in time. Please type '!form' to start over.")
            return
        
        #stopt de keys en de answers samen:
        answers_tup = list(zip(answers_keys, answers))
        
        await message.channel.send('Could you please check the answers and confirm that they are right?')

        #embed met user total answers
        descr = ""
        for i in range(n):
            if answers[i] == "":
                descr = descr + user_check[i] + answers[i] + "\n"
            else:
                descr = descr + user_check[i] + "``" + answers[i] + "``" + "\n"

        submitted=discord.Embed(title="Your submitted answers",
                    description=descr,
                     color=0xFF5733)
        await message.channel.send(embed=submitted)
        await message.channel.send('Type "Yes" or "No"')
        
        #confirmation vraag voor als alles goed is
        confirmation = await client.wait_for("message",check=check)
        if confirmation.content.upper() == "Y" or confirmation.content.upper() == "YES":
            #Write user inputs as row
            print(currentTime() + "File being generated...")

            if not os.path.exists("./user_answers/"):
                os.mkdir("./user_answers/")
            # else:
            #     print("User already has a directory")

            with open('./user_answers/{}.csv'.format(author), 'w', newline='') as file:
                # File writing
                writer = csv.writer(file)
                writer.writerow(header_ganesh)
                row = [""]*len(header_ganesh)
                
               
                #Zet de answer bij zijn bijbehorend kolom/key
                for i in range(len(header_ganesh)):
                    for j in range(len(answers_tup)):
                        if header_ganesh[i] ==  answers_tup[j][0]:
                            if answers_tup[j][1]=="!skip": #skip must show up as blank in the user_answers
                                row[i] = ""
                            else:
                                row[i] = answers_tup[j][1]
                            
                writer.writerow(row)
                file.close()
                
                print(currentTime() + u"\033[92mFile closed and generated.\n\u001b[0m" + currentTime() + "Sending file to channel...")
                # Logging and sending file to channel
                logger = client.get_channel(data['LOGGER'])
                await logger.send('CSV file generated for {}'.format(author))
                await logger.send(file=discord.File(r'./user_answers/{}.csv'.format(author)))
                print(currentTime() + u"\033[92mFile successfully sent to channel.\n\u001b[0m")
                await message.channel.send('Thank you for filling in the form! It has been sent to the admins.')

        else:
            await message.channel.send("Please fill in the form again by using !form.")
        
        
        
        print(user_amount)
        #Creation of user amount
        with open('./user_amount.csv', 'w', newline='') as file:
                        # File writing
            writer = csv.writer(file)
            for user in user_amount:
                #writes user -- amount in each row for when the bot is running
                writer.writerow(list(user))
            file.close()
        
        
        
        
        return


client.run(data['BOT_TOKEN'])