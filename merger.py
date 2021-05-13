import os
import csv


cd1 = "C:/Users/jorda/Desktop/Python/users_answers/"
cd2 = "C:/Users/jorda/Desktop/Python/files/"
ganesh = "Ganesh_template.csv"

#reading user_amount:
#nog niet AF:
with open('./user_amount.csv', 'r') as amountfile:
    reader1 = csv.reader(amountfile)
    header_ganesh = next(reader1)
print("Merging the answers of users....")




with open('./files/{}'.format(ganesh), 'r') as file:
    reader = csv.reader(file)
    header_ganesh = next(reader1)
print("Merging the answers of users....")


with open("Merged.csv", "w", newline='') as output:
    writer = csv.writer(output)
    writer.writerow(header_ganesh)
    for filename in os.listdir("./user_answers"):
        print(filename)
        with open('./user_answers/{}'.format(filename), 'r') as file:
            reader = csv.reader(file)
            if next(reader) != None:
                for row in reader:
                    writer.writerow(row)
    output.close()
                    

print("Merging the answers of users and corresponding amount....")
with open("Merged_amount.csv", "w", newline='') as output:
    writer = csv.writer(output)
    writer.writerow(header_ganesh)
    
    for filename in os.listdir("./user_answers"):
#        print(filename)
#        print(user_amount[teller][0])
#        print("Teller is", teller)
        for i in range(len(user_amount)):
            with open('./user_answers/{}'.format(filename), 'r') as file:
                print("File successfully opened")
                if filename == user_amount[i][0]:
                    reader = csv.reader(file)
                    if next(reader) != None:
                        for row in reader:
                            for i in range(int(user_amount[i][1])):
                                writer.writerow(row)
                        print("All rows written\n")
                        
    output.close()
                    