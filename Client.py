import requests

class PyBase:
    def __init__(self): # Constructor
        return # Nothing to store
    
    def __getitem__(self, item): # Method to get item by index [index (item) ]
        if item in self.__dict__: # Item does exist?
            return self.__dict__[item] # Return the item
    
    def __setitem__(self, item, data): # Method to update already stored item's data
        if item not in self.__dict__: # Item doesn't exist?
            return # Return
        
        self.__dict__[item] = data # Update the data for the existing item
    
    def __delitem__(self, item): # Method to delete item by index [index (item) ]
        if item in self.__dict__: # Item does exist?
            del self.__dict__[item] # Delete the item

class Client( PyBase ): # Client Class used to handle requests
    def __init__(self, mainUrl = str("http://localhost")): # Constructor

        if not isinstance(mainUrl, str): # Specified URL was not a string
            raise Exception("URL must be a type string!") # Raise Error (Exception)
        
        self.mainUrl = mainUrl # Store the main URL
        self.user = None # User attribute for API
    
    def sendReq(self, type = str("GET"), route = str(), json = {}, params = {}, cookies = {}): # Method used to send request to Server
        if not isinstance(type, str) or not isinstance(route, str): # Specified type or route is not a valid string
            return # Return
        
        req = None # Variable to store request
        
        try: # Try - catch | In case route / url is not resolved
            if "get" in type.lower(): # Type: GET
                req = requests.get(self.mainUrl + route, json=json, params=params, cookies=cookies)
            elif "post" in type.lower(): # Type: POST
                req = requests.post(self.mainUrl + route, json=json, params=params, cookies=cookies)
            elif "delete" in type.lower(): # Type: DELETE
                req = requests.delete(self.mainUrl + route, json=json, params=params, cookies=cookies)
        except:
            return req # Return 'None'
        
        if req is None or req.status_code == 404: # Invalid request?
            return print("Error resolving request!") # Return 'None' ( print() -> None )
        
        data = req.json() # Get JSON data from requested response
        return data # Return data