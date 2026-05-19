import dolphin_memory_engine
import time
from src.RidersPyTools_KC.include.Constants import GameIDs
import GameState

# def dolphin_connection_proc():
print("Attempting to connect to Dolphin...")
print("If Dolphin is not open, open it now, or close this program.")
dolphin_memory_engine.hook()
if dolphin_memory_engine.is_hooked():
    # Hook and check the game (convert to async def later)
    game_id_bytes = dolphin_memory_engine.read_bytes(0x80000000, 6)
    print("Checking game version...")
    # Match case did not let me convert to bytes here so, lmao I don't using an if-statement but sure man whatever.
    match game_id_bytes:
        case GameIDs.SONIC_RIDERS_ID:
            GameState.GAME_VERSION = GameIDs.SONIC_RIDERS_ID
            print("Game loaded: Sonic Riders (Vanilla/Vanilla based mod)")

        case GameIDs.SONIC_RIDERS_TE_ID:
            GameState.GAME_VERSION = GameIDs.SONIC_RIDERS_TE_ID
            print("Game loaded: Sonic Riders: Tournament Edition")

        case GameIDs.SONIC_RIDERS_DX_ID:
            GameState.GAME_VERSION = GameIDs.SONIC_RIDERS_DX_ID
            print("Game loaded: Sonic Riders: DX")

        case GameIDs.SONIC_RIDERS_ZG_ID:
            GameState.GAME_VERSION = GameIDs.SONIC_RIDERS_ZG_ID
            print("Game loaded: Sonic Riders: Zero Gravity")

        case GameIDs.SONIC_RIDERS_FT_ID:
            GameState.GAME_VERSION = GameIDs.SONIC_RIDERS_FT_ID
            print("Game loaded: Sonic Riders: Future")

        case _:
            print("No valid Sonic Riders game loaded in this dolphin instance, please load a supported Sonic Riders version.")
            dolphin_memory_engine.un_hook()
            pass

    # if game_id_bytes == bytes(SONIC_RIDERS_ID, "utf-8"):
    #     GameState.GAME_VERSION = GameVersion.Vanilla
    #     print("Game loaded: Sonic Riders (Vanilla/Vanilla based mod)")
    # elif bytes(SONIC_RIDERS_TE_ID, "utf-8"):
    #     GameState.GAME_VERSION = GameVersion.TE
    #     print("Game loaded: Sonic Riders: Tournament Edition")
    # elif bytes(SONIC_RIDERS_DX_ID, "utf-8"):
    #     GameState.GAME_VERSION = GameVersion.DX
    #     print("Game loaded: Sonic Riders: DX")
    # elif bytes(SONIC_RIDERS_ZG_ID, "utf-8"):
    #     GameState.GAME_VERSION = GameVersion.ZG
    #     print("Game loaded: Sonic Riders: Zero Gravity")
    # else:
    #     print("No valid Sonic Riders game loaded, please load a valid Sonic Riders ROM.")
    #     dolphin_memory_engine.un_hook()

else:
    print("Connection to Dolphin failed, attempting again in 5 seconds...")
    time.sleep(5)
    # dolphin_connection_proc()
pass