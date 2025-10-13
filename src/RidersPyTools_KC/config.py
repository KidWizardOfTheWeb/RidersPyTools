# In this file, we hold the settings for whatever the user does.
# This is particularly important in order to keep a possible main.map as a global variable for reference

import MapParser

MAIN_MAP_FILE = None # If there is a main.map set before the script, set to true.
SYMBOL_ACCESS_LEVEL = 0 # levels change, but assume 0 means player ptrs only, while higher values are more elevated access.


"""
If the user sets this, we can set this value to the MainMapFile given.
Else, just use vanilla ptrs, since only TE as of now changes the mem locs. DX-based builds only allocate more.
"""
def SetMainMap(pathToMapFile):
    # Run the map parser here so we can store the symbols needed for later in a dictionary.
    MapParser.read_for_files(pathToMapFile)
    # Store symbols in the object listing, somehow.
    global MAIN_MAP_FILE
    MAIN_MAP_FILE = pathToMapFile
    pass

"""
The user will not need to set this value unless they're a power user
0 = player pointers only. No other values can be modified, only read.
1 = player ptrs + player related values. No other values can be modified, only read.
2 = Unlimited access. Read/Write has zero restrictions. Users with this active better take care not to do anything crazy.
"""
def SetSymbolAccessLevel(levelToSet):
    if levelToSet < 0 or levelToSet > 2:
        print("Symbol access level invalid. Please set a number 0-2")
        return
    global SYMBOL_ACCESS_LEVEL
    SYMBOL_ACCESS_LEVEL = levelToSet
    pass

