from src.RidersPyTools_KC.Characters import CHR_ID_TO_NAME, CHR_ID_TO_DEFAULT_GEAR_NAME
from src.RidersPyTools_KC.GameState import RaceState, ExitMethod, MODE_ID_TO_NAME, GameModes
from src.RidersPyTools_KC.Gears import GEAR_ID_TO_NAME, ALL_GEARS
from src.RidersPyTools_KC.Stages import STAGE_ID_TO_NAME
from src.RidersPyTools_KC.Archetypes import ARCH_ID_TO_NAME
from src.RidersPyTools_KC.Player import Player, DME
from src.RidersPyTools_KC.RidersObject import RidersObject
from src.RidersPyTools_KC.include.Constants import *

# Python imports
from pypresence import Presence, PyPresenceException
import time

def RPC_loop(client_id):
    DME.hook()

    player1 = Player(0, TE_PLAYER_PTR)

    # These overrides are for TE 2.4.6.1
    # Add a command line param to enable/disable these maybe?
    object_overrides = {
        "CurrentGameMode": 0x8053C2E0,
        "geGame_ModeDetail": 0x8053C2E4,
        "CurrentStage": 0x8053C2E8,
        "ExitMethod": 0x8053C300,
        "StageTimer": 0x8053C480
    }
    ridersObject1 = RidersObject(object_overrides)

    RPC = Presence(client_id=client_id)  # Initialize the client class
    RPC.connect()  # Start the handshake loop

    while True:  # The presence will stay on as long as the program is running
        """
        Things to get:
        1. Game and mod version.
        2. Mode.
        3. Stage (and image). 
        4. Current time.
        5. If 1P, activity_type == "Playing". If 2P+, activity_type == "Competing"
        """

        game_id = ridersObject1.gameID
        game_name = GAME_ID_TO_NAME[GameIDs(bytes(game_id))]

        current_mode_id = int(ridersObject1.currentMode)
        current_mode = MODE_ID_TO_NAME[current_mode_id]

        stage_name = STAGE_ID_TO_NAME[ridersObject1.currentStage]

        current_lap = int(player1.currentLap)

        # TODO: add TE-specific/other mod specific structs if vanilla characters don't check out.
        # Get game version with game_name variable from above, use that to select a dict
        try:
            character = CHR_ID_TO_NAME[player1.character]
        except KeyError:
            character = str(player1.character)

        try:
            gear = GEAR_ID_TO_NAME[player1.extremeGear]
        except KeyError:
            gear = str(player1.extremeGear)

        small_image = ""
        small_string = ""
        
        if gear == GEAR_ID_TO_NAME[255]:
            # invalid gear
            small_string = str(character + ", selecting a gear.")
            small_image = str(character).lower() + "_default"
        elif gear == GEAR_ID_TO_NAME[0]:
            # If default gear, set string to char_default.
            small_image = str(character).lower() + "_default"

            try:
                gear = CHR_ID_TO_DEFAULT_GEAR_NAME[player1.character]
            except KeyError:
                gear = GEAR_ID_TO_NAME[0]
            small_string = str(character + " and " + gear)
        else:
            # TODO: use a translation map instead of multiple replacements
            small_image = gear.replace(" ", "_").lower()
            # Any extra characters like the apostrophe should also be removed for Board '70
            small_image = small_image.replace("'", "")
            # Covers e-rider
            small_image = small_image.replace("-", "_")
            small_string = str(character + " and " + gear)

        lap_string = ""
        if current_mode_id is not int(GameModes.TITLE_SCREEN) and current_mode_id is not int(GameModes.BATTLE_MODE) and current_mode_id is not int(GameModes.CUTSCENE_MODE):
            lap_string = " - Race Start" if current_lap == 0 else " - Lap {}".format(current_lap)

        RPC.update(
            details=current_mode + lap_string,
            state=stage_name,
            large_image=stage_name.replace(" ", "_").lower(),
            large_text=stage_name,
            small_image=small_image,
            small_text=small_string,
            name=game_name
        )
        time.sleep(5)  # Can only update rich presence every X seconds

if __name__ == "__main__":
    RPC_loop(1507118425951174706)