from tkinter import * # Tkinter API
from Client import PyBase # PyBase Class

class Vec2( PyBase ): # Vector2 -> X, Y
    def __init__(self, x = 0, y = 0): # Constructor
        self.x = x # LEFT -> RIGHT 
        self.y = y # TOP -> BOTTOM

class WindowHandler: # Window Handler Class (Using Tkinter)
    def __init__(self): # Constructor
        self.root = None                                                     # Main Window
        self.windows = []                                                    # List of Windows

        self.root = self.createWin(                                          # Create the root parent Window
            title = str("Main Window"),                                      # Main Window Tile
        )

        self.editWin(self.root,                                              # Edit Main Window
            backgroundColor = "#161717",                                     # Set background color
            size = Vec2(650, 650),                                           # Set size
            zoomed = True
        )
    
    def __getitem__(self, item):
        if type(item) == Tk:                                                 # Specifier is a Tkinter Window type
            for window in self.windows:                                      # Iterate over Windows
                if window == item:                                           # Window instance matches specifier
                    return window                                            # Return the Window
                    
        elif type(item) == int:                                              # Specifier was type int, get by index
            if item > (len(self.windows) - 1):
                return print("Range is out of bounds!")                      # Index is out of range
            return self.windows[item]                                        # Return the Window from index
    
    def onWindowClose(self, window):
        iterator = int(0)                                                    # Iteration Count in Loop
        
        for w in self.windows:
            if w == window:                                                  # Found Window from list
                del self.windows[iterator]                                   # Delete from list
                break
            iterator += 1                                                    # Increment Iterator
        
        window.destroy()                                                     # Destroy Window Instance
    
    def createWin(self, title = str("Window"), zoomed = False):              # Create new Tkinter Window
        newWindow = None

        for window in self.windows:                                          # Iterate over existing Windows
            if window.title() == title:                                      # Window with that title already exists
                newWindow = window                                           # Assign instance to variable so it can be returned as it already exists
        
        if newWindow is None:
            newWindow = Tk()                                                 # Create the new Window
            newWindow.title(title)                                           # Set Window Title

            newWindow.protocol("WM_DELETE_WINDOW",                           # Window on close event
                lambda w = newWindow:                                        # Lambda Expression, use current instance and assign to lambda variable
                    self.onWindowClose(newWindow)                            # Call onClose method to handle event
                )

            self.windows.append(newWindow)                                   # Append the new Window instance to list
        
        if zoomed:
            newWindow.state("zoomed")                                        # Full screen Window
        
        return newWindow                                                     # Return the Window instance
    
    def editWin(self, window, title = None, size = None, backgroundColor = None, zoomed = False, topMost = False):
        if not isinstance(window, Tk):
            return print("You did not specify a Window!")                    # No Window Instance was specified
        
        if isinstance(size, Vec2) and size.x > 0 and size.y > 0:             # Window Position was specified?
            window.geometry(f"{size['x']}x{size['y']}")                      # Set the Window size
        
        if isinstance(title, str) and len(title) > 0:                        # Window title was specified?
            window.title(title)                                              # Set the Window size
        
        if isinstance(backgroundColor, str) and len(backgroundColor) > 0:    # Window background color was specified?
            window.config(bg = backgroundColor)                              # Set Window Color
        
        if zoomed:                                                           # Window Fullscreen was specified?
            window.state("zoomed")                                           # Fullscreen Window
        
        if topMost:                                                          # Window above others was specified?
            window.attributes("-topmost", True)                              # Shift above others
    
    def clearWinElements(self, window, exclude = []):
        if not isinstance(window, Tk) and not isinstance(window, Frame):     # Validate type
            return print("You did not specify a Window!")                    # No Window Instance was specified
        
        if isinstance(window, Tk):                                           # Element given was a window instance
            for widget in window.winfo_children():                           # Iterate over window contents
                if type(widget) in exclude:                                  # Type is in filter?
                    continue                                                 # Skip
                widget.destroy()                                             # If not, destroy!
        
        elif isinstance(window, Frame):                                      # Element given was a frame instance
            for widget in window.winfo_children():                           # Iterate over frame contents
                if type(widget) in exclude:                                  # Type is in filter?
                    continue                                                 # Skip
                widget.destroy()                                             # If not, destroy!