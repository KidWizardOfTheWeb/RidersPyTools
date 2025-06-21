import dolphin_memory_engine
import time
from Constants import *

# def dolphin_connection_proc():
print("Attempting to connect to Dolphin...")
dolphin_memory_engine.hook()
if dolphin_memory_engine.is_hooked():
    # Hook and check the game
    game_id_bytes = dolphin_memory_engine.read_bytes(0x80000000, 6)
    print("Checking game version...")
    # Match case did not let me convert to bytes here so, lmao I don't like this but sure man whatever.
    if game_id_bytes == bytes(SONIC_RIDERS_ID, "utf-8"):
        print("Game loaded: Sonic Riders (Vanilla/Vanilla based mod)")
    elif bytes(SONIC_RIDERS_TE_ID, "utf-8"):
        print("Game loaded: Sonic Riders: Tournament Edition")
    elif bytes(SONIC_RIDERS_DX_ID, "utf-8"):
        print("Game loaded: Sonic Riders: DX")
    elif bytes(SONIC_RIDERS_ZG_ID, "utf-8"):
        print("Game loaded: Sonic Riders: Zero Gravity")
    else:
        print("No valid Sonic Riders game loaded, please load a valid Sonic Riders ROM.")
        dolphin_memory_engine.un_hook()
else:
    print("Connection to Dolphin failed, attempting again in 5 seconds...")
    time.sleep(5)
    # dolphin_connection_proc()
pass