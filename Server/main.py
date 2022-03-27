from flask import Flask, make_response, request # Flask API
from ClientDB import * # Create Databases (For Flask Server End)
import bcrypt # Password Hashing
import uuid as UUID # Generate Unique ID's
import re # Regex

app = Flask(__name__) # Flask App Instance
users = ClientDB("Users") # Users Database

@app.route("/register", methods = ["POST"]) # Register Route
def register():
    
    returnData = {
        "User": None, # User Object (If Successful)
        "Response": None # Response, if failed
    }

    email = request.args.get("email") # Email
    nick = request.args.get("nick")   # Username
    psw = request.args.get("pass")    # Password

    '''
        Validate Provided Email from Request
    '''

    if not isinstance(email, str): # Provided Email is not a string
        returnData["Response"] = "Email must be a string!"
        return returnData # Return Response
    
    if len(email) > 30: # Provided Email has exceeded max length
        returnData["Response"] = "Email cannot be greater than 30 characters!"
        return returnData # Return Response
    
    if not re.match("[^@]+@[^@]+\.[^@]+", str(email).lower()): # Email is not valid!
        returnData["Response"] = "Provided Email is not valid!"
        return returnData # Return Response
    
    '''
        Validate Provided Username (Nick) from Request
    '''
    
    if not isinstance(nick, str): # Provided Nick is not a string
        returnData["Response"] = "Nick must be a string!"
        return returnData # Return Response
    
    if len(nick) > 12: # Provided Nick has exceeded max length
        returnData["Response"] = "Nick cannot be greater than 12 characters!"
        return returnData # Return Response
    
    '''
        Validate Provided Password from Request
    '''
    
    if not isinstance(psw, str): # Provided Pass is not a string
        returnData["Response"] = "Pass must be a string!"
        return returnData # Return Response
    
    if len(psw) > 12: # Provided Password has exceeded max length
        returnData["Response"] = "Pass cannot be greater than 12 characters!"
        return returnData # Return Response
    
    '''
        Validate whether email or username have been taken
    '''
    
    if len(users[None]) > 0:
        for uuid in users[None]: # Iterate over user uuids
            user = users[uuid] # Current User
            if user["email"] == str(email).lower(): # Email taken?
                returnData["Response"] = "Email has already been taken!"
                return returnData # Return Response
            if str(user["nick"]).lower() == str(nick).lower(): # Nick taken?
                returnData["Response"] = "Nick has already been taken!"
                return returnData # Return Response
    
    '''
        Encrypt Password
    '''

    salt = bcrypt.gensalt() # Salt for Hash
    hash = bcrypt.hashpw(psw.encode(), salt) # Encrypt raw password

    userUUID = str(UUID.uuid4()) # Generate UUID for User
    users[userUUID] = { # Store User to Database
        "email": str(email).lower(), # Email
        "nick": nick, # Username
        "uuid": userUUID, # User ID
        "friends": {}, # Friends list
        "hash": str(hash.decode()) # Encrypted Hash, used to validate requests
    }

    returnData["User"] = users[userUUID] # Set User Object for Request Result
    return returnData # Return Response

@app.route("/login", methods = ["POST"]) # Login route
def login():
    returnData = {
        "User": None, # User Object (If Successful)
        "Response": None # Response, if failed
    }

    email = request.args.get("email") # Email
    psw = request.args.get("pass")    # Password

    '''
        Validate Provided Email from Request
    '''

    if not isinstance(email, str): # Provided Email is not a string
        returnData["Response"] = "Email must be a string!"
        return returnData # Return Response
    
    if len(email) > 30: # Provided Email has exceeded max length
        returnData["Response"] = "Email cannot be greater than 30 characters!"
        return returnData # Return Response
    
    if not re.match("[^@]+@[^@]+\.[^@]+", str(email).lower()): # Email is not valid!
        returnData["Response"] = "Provided Email is not valid!"
        return returnData # Return Response
    
    '''
        Validate Provided Password from Request
    '''
    
    if not isinstance(psw, str): # Provided Pass is not a string
        returnData["Response"] = "Pass must be a string!"
        return returnData # Return Response
    
    if len(psw) > 12: # Provided Password has exceeded max length
        returnData["Response"] = "Pass cannot be greater than 12 characters!"
        return returnData # Return Response
    
    '''
        Check if account exists
    '''

    found = None # Instance to found user
    
    if len(users[None]) > 0: # Iterate over users to see if account exists or not
        for uuid in users[None]: # Iterate over user uuids
            user = users[uuid] # Current User
            if user["email"] == str(email).lower(): # Email taken?
                found = user # assign current instance to 'Found'
                break # Stop iterating

    if found is None:
        returnData["Response"] = "No account exists with that Email!"
        return returnData
    
    '''
        Compare provided Password
    '''
    
    if bcrypt.checkpw(psw.encode(), str(found["hash"]).encode()):
        returnData["Response"] = "Successfully logged in!" # Correct Password!
        returnData["User"] = found
    else:
        returnData["Response"] = "Incorrect Password!" # Incorrect Password
    
    return returnData # Return Data

@app.route("/validate_token", methods = ["GET"]) # Validate Token Route
def validateToken():
    
    returnData = {
        "User": None, # User Object (If Successful)
        "Response": None # Response, if failed
    }
    
    hash = request.args.get("hash")

    if hash is None:
        returnData["Response"] = "Token was not specified!"
        return returnData # Return data
    
    if not isinstance(hash, str) or len(hash) > 200:
        returnData["Response"] = "Token is not valid!"
        return returnData # Return data
    
    found = None # Instance of user
    usersList = users[None] # List of users
    
    for uuid in usersList: # Iterate over user uuids
        user = usersList[uuid] # Current User

        if user["hash"] == hash: # Hash matches
            found = user # Assign 'User' to found variable
            break # Stop the loop
    
    if found is None: # Couldn't find user with that token
        returnData["Response"] = "Could not find a User with that token!"
        return returnData # Return data
    
    returnData["User"] = found # User was found
    returnData["Response"] = "Successfully verified token!"

    return returnData # Return data

# Main Driver Function
if __name__ == "__main__":
    app.run(debug = False, port=80)