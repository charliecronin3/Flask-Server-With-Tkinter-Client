from pathlib import Path
import ast
import os

class ClientDB:
    def __init__(self, name = str("DB")):
        
        if not isinstance(name, str) or len(name) <= 0: # Specified name was not valid
            name = str("DB") # Set name back to default
        
        self.name = name # Set Database name
        self.path = Path(f"{name}.txt") # Set File Path
        
        self.validateFile() # Create File if non existent
        
    def validateFile(self): # Method used to create file if non existent
        if self.path.exists() == False: # File doesn't exist
            with open(self.path, "x") as f: # Create file
                f.write(str(dict())) # Store dict
                f.close() # Close file as it's been created
        else:
            with open(self.path, "r+") as f: # Read & Write file
                if len(f.readline()) <= 0: # File empty?
                    f.close() # Close File so we can delete it
                    os.remove(self.path) # Delete File
                    self.validateFile() # Create file with propper contents
    
    def __getitem__(self, item):
        self.validateFile() # Create File if non existent

        with open(self.path) as f: # Open file
            cache = ast.literal_eval(f.readline()) # Cache database contents

            if item is None: # Item is None
                return cache # Return all

            if item in cache: # Found item!
                return cache[item] # Return item

        return None # Clearly didn't find, return nothing
    
    def __setitem__(self, item, data):
        self.validateFile() # Create File if non existent

        with open(self.path) as f: # Open file
            cache = ast.literal_eval(f.readline()) # Cache database contents
            cache[item] = data # Set cached data
            
            with open(self.path, "r+") as _f: # Read file
                _f.write(str(cache)) # Store updated contents to database
    
    def __delitem__(self, item):
        self.validateFile() # Create File if non existent

        with open(self.path) as f: # Open file
            cache = ast.literal_eval(f.readline()) # Cache database contents

            if item in cache:
                del cache[item]

                with open(self.path, "w") as _f: # Read file
                    _f.write(str(cache)) # Store updated contents to database