from Client import *                                                                                    # Handle Requests
from WindowHandler import *                                                                             # Handle Tkinter Windows

from ClientDB import *                                                                                  # Handle Auth Data

client = Client()                                                                                       # Declare instance of Client (Used for request handling)
wh = WindowHandler()                                                                                    # Declare instance of WindowHandler
user = ClientDB("User")                                                                                 # Declare Instance of ClientDB (To save auth data)

wh.root.minsize(300, 300)                                                                               # Min Window Size for main window

def displayLogin():
    
    wh.clearWinElements(wh.root)                                                                        # Clear window elements

    emailEntry = StringVar()                                                                            # StringVar instance for email entry
    pswEntry = StringVar()                                                                              # StringVar instance for password entry

    errorMsg = StringVar()                                                                              # StringVar instance for error message label
    errorMsgLbl = Label(wh.root, textvariable=errorMsg, width=36, bg="#0ecccc", font=("Arial", 16))     # Error message label

    def login():                                                                                        # Login Function

        errorMsgLbl.pack(padx=10, pady=10)                                                              # Display visibility of error message label
        
        email = emailEntry.get()                                                                        # Get value from email entry
        psw = pswEntry.get()                                                                            # Get value from password entry

        if len(email) <= 0:                                                                             # Validate if email was specified
            return errorMsg.set("Email was not specified!")                                             # Email was not specified!
        
        if len(email) > 30:                                                                             # Email exceeds max chars?
            return errorMsg.set("Email cannot exceed 30 chars!")                                        # Email does exceed max chars!
        
        if len(psw) <= 0:                                                                               # Validate if password was specified
            return errorMsg.set("Password was not specified!")                                          # Password was not specified!
        
        if len(psw) > 12:                                                                               # Password exceeds max chars!
            return errorMsg.set("Password cannot exceed 12 chars!")                                     # Password does exceed max chars!

        req = client.sendReq(                                                                           # Send login request
            type = str("POST"),                                                                         # Type: POST
            route = str("/login"),                                                                      # Route: /login
            params = {                                                                                  # Params added to route url
                "email": email,                                                                         # Email specified
                "pass": psw                                                                             # Password specified
            }
        )

        if req is None or "User" not in req or "Response" not in req:                                   # Validate request response
            return errorMsg.set("Error resolving request!")                                             # Throw error
        
        if req["User"] is None or "hash" not in req["User"]:                                            # Validate if successful
            return errorMsg.set(req["Response"])                                                        # Throw response message
        else:
            user["Hash"] = req["User"]["hash"]                                                          # Was successful, store data
            return displayMain()                                                                        # Show main contents
            
    frame = Frame(wh.root)                                                                              # Declare instance of frame used to position register button
    
    Button(                                                                                             # Declare instance of button to display register elements
        frame,
        text="Register",
        width=26,
        bg="#0ecccc",
        font=("Arial", 16),
        command=displayRegister
    ).pack(in_=frame)                                                                                   # Position Register Button

    frame.pack(side="bottom", anchor=SE, pady=10, padx=10)                                              # Position Frame for Register button to bottom left

    frameA = Frame(wh.root)                                                                             # Frame for Username elements
    frameB = Frame(wh.root)                                                                             # Frame for password elements

    Label(                                                                                              # Email Label
        frameA, text="Email", width=10, bg="#0ecccc", font=("Arial", 16)
    ).pack(in_=frameA, side=LEFT)                                                                       # Position Email Label

    Entry(                                                                                              # Email Entry
        frameA, textvariable=emailEntry, width=26, bg="#0ecccc", font=("Arial", 16)
    ).pack(in_=frameA, side=LEFT)                                                                       # Position Email Entry

    Label(                                                                                              # Password Label
        frameB, text="Password", width=10, bg="#0ecccc", font=("Arial", 16)
    ).pack(in_=frameB, side=LEFT)                                                                       # Position Password Label

    Entry(                                                                                              # Password Entry
        frameB, textvariable=pswEntry, width=26, bg="#0ecccc", font=("Arial", 16), show="*"
    ).pack(in_=frameB, side=LEFT)                                                                       # Position Password Entry

    frameA.pack(padx=10, pady=10)                                                                       # Position frame for username elements
    frameB.pack(padx=10, pady=10)                                                                       # Position frame for password elements

    loginBtn = Button(                                                                                  # Button to authenticate
        wh.root, text="Login", width=36, bg="#0ecccc", font=("Arial", 16), command=login
    )

    loginBtn.pack(padx=10, pady=10)                                                                     # Position login button

def displayRegister():
    
    wh.clearWinElements(wh.root)                                                                        # Clear window elements

    emailEntry = StringVar()                                                                            # StringVar instance for email entry
    nickEntry = StringVar()                                                                             # StringVar instance for username entry
    pswEntry = StringVar()                                                                              # StringVar instance for password entry

    errorMsg = StringVar()                                                                              # StringVar instance for error message label
    errorMsgLbl = Label(wh.root, textvariable=errorMsg, width=36, bg="#0ecccc", font=("Arial", 16))     # Error message label

    def register():                                                                                     # Register Function

        errorMsgLbl.pack(padx=10, pady=10)                                                              # Display visibility of error message label
        
        email = emailEntry.get()                                                                        # Get value from email entry
        nick = nickEntry.get()                                                                          # Get value from username entry
        psw = pswEntry.get()                                                                            # Get value from password entry

        if len(email) <= 0:                                                                             # Validate if email was specified
            return errorMsg.set("Email was not specified!")                                             # Email was not specified!
        
        if len(email) > 30:                                                                             # Email exceeds max chars?
            return errorMsg.set("Email cannot exceed 30 chars!")                                        # Email does exceed max chars!
        
        if len(nick) <= 0:                                                                              # Validate if Username was specified
            return errorMsg.set("Username was not specified!")                                          # Username was not specified!
        
        if len(nick) > 12:                                                                              # Username exceeds max chars?
            return errorMsg.set("Username cannot exceed 30 chars!")                                     # Username does exceed max chars!
        
        if len(psw) <= 0:                                                                               # Validate if password was specified
            return errorMsg.set("Password was not specified!")                                          # Password was not specified!
        
        if len(psw) > 12:                                                                               # Password exceeds max chars!
            return errorMsg.set("Password cannot exceed 12 chars!")                                     # Password does exceed max chars!

        req = client.sendReq(                                                                           # Send register request
            type = str("POST"),                                                                         # Type: POST
            route = str("/register"),                                                                   # Route: /register
            params = {                                                                                  # Params added to route url
                "email": email,                                                                         # Email specified
                "nick": nick,                                                                           # Username specified
                "pass": psw                                                                             # Password specified
            }
        )

        if req is None or "User" not in req or "Response" not in req:                                   # Validate request response
            return errorMsg.set("Error resolving request!")                                             # Throw error
        
        if req["User"] is None or "hash" not in req["User"]:                                            # Validate if successful
            return errorMsg.set(req["Response"])                                                        # Throw response message
        else:
            user["Hash"] = req["User"]["hash"]                                                          # Was successful, store data
            return displayMain()                                                                        # Show main contents
    
    frame = Frame(wh.root)                                                                              # Declare instance of frame used to position login button
    
    Button(                                                                                             # Declare instance of button to display login elements
        frame,
        text="Login",
        width=26,
        bg="#0ecccc",
        font=("Arial", 16),
        command=displayLogin
    ).pack(in_=frame)                                                                                   # Position Login Button

    frame.pack(side="bottom", anchor=SE, pady=10, padx=10)                                              # Position Frame for Register button to bottom left

    frameA = Frame(wh.root)                                                                             # Frame for Username elements
    frameB = Frame(wh.root)                                                                             # Frame for username elements
    frameC = Frame(wh.root)                                                                             # Frame for password elements

    Label(                                                                                              # Email Label
        frameA, text="Email", width=10, bg="#0ecccc", font=("Arial", 16)
    ).pack(in_=frameA, side=LEFT)                                                                       # Position Email Label

    Entry(                                                                                              # Email Entry
        frameA, textvariable=emailEntry, width=26, bg="#0ecccc", font=("Arial", 16)
    ).pack(in_=frameA, side=LEFT)                                                                       # Position Email Entry

    Label(                                                                                              # Email Label
        frameB, text="Username", width=10, bg="#0ecccc", font=("Arial", 16)
    ).pack(in_=frameB, side=LEFT)                                                                       # Position Email Label

    Entry(                                                                                              # Username Entry
        frameB, textvariable=nickEntry, width=26, bg="#0ecccc", font=("Arial", 16)
    ).pack(in_=frameB, side=LEFT)                                                                       # Position Username Entry

    Label(                                                                                              # Password Label
        frameC, text="Password", width=10, bg="#0ecccc", font=("Arial", 16)
    ).pack(in_=frameC, side=LEFT)                                                                       # Position Password Label

    Entry(                                                                                              # Password Entry
        frameC, textvariable=pswEntry, width=26, bg="#0ecccc", font=("Arial", 16), show="*"
    ).pack(in_=frameC, side=LEFT)                                                                       # Position Password Entry

    frameA.pack(padx=10, pady=10)                                                                       # Position frame for username elements
    frameB.pack(padx=10, pady=10)                                                                       # Position frame for username elements
    frameC.pack(padx=10, pady=10)                                                                       # Position frame for password elements

    registerBtn = Button(                                                                               # Button to authenticate
        wh.root, text="Register", width=36, bg="#0ecccc", font=("Arial", 16), command=register
    )

    registerBtn.pack(padx=10, pady=10)                                                                  # Position register button

def displayAuth():                                                                                      # Display Login / Register elements

    wh.clearWinElements(wh.root)                                                                        # Clear window elements

    frame = Frame(wh.root)                                                                              # Create frame to stick buttons together
    
    Button(                                                                                             # Login Button
        frame, text=str("Login"), width=10, bg="#0ecccc", font=("Arial", 16), command=displayLogin
    ).pack(in_=frame, side=LEFT)                                                                        # Position login button
    
    Button(                                                                                             # Register Button
        frame, text=str("Register"), width=10, bg="#0ecccc", font=("Arial", 16), command=displayRegister
    ).pack(in_=frame, side=LEFT)                                                                        # Position register button

    frame.pack(padx=10, pady=10)                                                                        # Positon frame with buttons included

def onTick():                                                                                           # Keep getting 'Client' user data

    if user["Hash"] is None:                                                                            # If saved hash doesn't exist, show auth options
        return displayAuth()                                                                            # Show auth options
    
    req = client.sendReq(                                                                               # Send request to validate token (hash)
        type = str("GET"),                                                                              # Type: GET
        route = str("/validate_token"),                                                                 # Route: /validate_token
        params = {                                                                                      # Params added to route url
            "hash": user["Hash"]
        }
    )

    if req is None:                                                                                     # Request failed, show auth options
        return displayAuth()                                                                            # Show auth options
    else:
        if req["User"] is None:
            return displayAuth()                                                                        # Show auth options
        else:
            if "hash" in req["User"]:                                                                   # Request was successful and token was valid
                user["Hash"] = req["User"]["hash"]                                                      # Save token (hash)
                client["user"] = req["User"]                                                            # Cache user data
    
    wh.root.after(10000, onTick)                                                                        # Validate token every 10 seconds

def displayMain():                                                                                      # Display main contents

    wh.clearWinElements(wh.root)                                                                        # Clear window elements
    onTick()                                                                                            # Call ontick

    if client["user"] is None:                                                                          # User is invalid?
        return                                                                                          # Return as user is invalid :/

    Label(                                                                                              # Label to display username
        wh.root, text=str(client["user"]["nick"]), width=1000, bg="#2da174", font=("Arial", 12)
    ).pack(padx=10)                                                                                     # Position username label

displayMain()                                                                                           # Call main
wh.root.mainloop()                                                                                      # Render Main Window