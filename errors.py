import re

errormessage = ""

# Add more constraints as security so people cant inject any statements or functions
# The values we use are strings (message.content) so it shouldnt really be possible to abuse
def checkerrors(reply,key):
    global errormessage
    # Amount of pairs = only a number, no letter inputs
    # Check that it is in the values list (1-100)
    if key == "AMOUNT":
        values = [i for i in range(1,101)]
        if reply.isnumeric() and int(reply) in values:
            # print("User requested {} pairs".format(int(reply)))
            return True
        errormessage = "Your input was not an integer"
        print("User did not input an integer")
        return False

    # Names = 1 to 2 words, no numbers
    elif key == ("FIRST NAME") or key == ("LAST NAME"):
        containsNumber = any(char.isdigit() for char in reply)
        if containsNumber == False:
            errormessage = "Your answer had too many words"
            length = len(reply.split())
            # print("Length of the string is {} words, the content of the string is {}".format(length,reply))
            # print("Content of the string is {}".format(reply))
            return length <= 2
        errormessage = "First or last name can not contain numbers"
        return False

    # Use email checker function for valid emails
    elif key == "EMAIL":
        errormessage = "That is not a valid email"
        return (re.match("^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$", reply) != None)

    # Phone number = no symbols, only numbers - max(x characters)
    elif key == "PHONE NUMBER":
        errormessage = "Phone number can not have spaces and it has to be less than 13 characters"
        return (reply.isnumeric() and (len(reply.split()) <= 1) and (7 < len(reply) <= 13))

    # Address line 1 = max(21 characters)
    elif key == "ADDRESS LINE 1":
        errormessage = "Address line 1 has to be shorter than 21 characters"
        return (len(reply) <= 21)

    # Address line 2 = max(13 characters)
    elif key == "ADDRESS LINE 2":
        errormessage = "Address line 2 has to be shorter than 13 characters"
        return (len(reply) <= 13)

    # City (No numbers) = string
    elif key == "CITY":
        errormessage = "Your answer contained numbers or it was too long"
        return ((len(reply) <= 20) and not(any(char.isdigit() for char in reply)))

    # State => return null value back to the answers array with tuples later on
    elif key == "STATE":
        errormessage = "Your answer contained numbers or it was too long"
        return ((len(reply) <= 16) and not(any(char.isdigit() for char in reply)))

    # Postal code
    elif key == "POSTCODE / ZIP":
        errormessage = "Your input was too long"
        return (len(reply) <= 12)

    # Country = check list of correct country abbreviations and compare it to user input
    elif key == "COUNTRY":
        errormessage = "Country abbreviation has to be 2 letters"
        regions = ["NL","AU","GR","SE","PT","IT","PL","CZ","GB","UK","HU","DE","NO","AT","BE","FR","ES","US", "CA"]
        if len(reply) == 2:
            # print("Country is 2 letters")
            for region in regions:
                if reply.upper() == region:
                    return True
        return False

    # Credit card number = 1234123412341234 = 16 chars no spaces
    elif key == "CARD NUMBER":
        errormessage = "Card number has to be 16 digits without spaces"
        return (reply.isnumeric() and len(reply) == 16 and (len(reply.split()) == 1))

    # Expiry month = 2 digits, not more not less =  between 01 and 12
    elif key == "EXPIRE MONTH":
        errormessage = "Month has to be 2 digits"
        months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
        return (reply.isnumeric() and (reply in months))

    # Expiry year = 4 digits, not more not less = greater than or equal to 2021
    elif key == "EXPIRE YEAR":
        errormessage = "Year has to be 4 digits"
        return (reply.isnumeric() and (len(reply.split()) == 1) and (len(reply) == 4) and (int(reply) >= 2021))

    # CVC = 3 digits, not more not less
    elif key == "CARD CVC":
        errormessage = "You can only input 3 digits"
        return (reply.isnumeric() and (len(reply.split()) == 1) and (len(reply) == 3))