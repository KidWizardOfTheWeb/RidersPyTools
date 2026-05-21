from src.RidersPyTools_KC.Characters import CHR_ID_TO_NAME
from src.RidersPyTools_KC.Gears import GEAR_ID_TO_NAME
from src.RidersPyTools_KC.Stages import STAGE_ID_TO_NAME
from src.RidersPyTools_KC.Archetypes import ARCH_ID_TO_NAME
from src.RidersPyTools_KC.Player import Player, DME
from src.RidersPyTools_KC.RidersObject import RidersObject
from src.RidersPyTools_KC.include.Constants import *

import time

if __name__ == "__main__":
    # Hook Dolphin here
    DME.hook()

    # Instantiate player ptr on py side
    player1 = Player(0, TE_PLAYER_PTR)

    # Instantiate the stage timer for 2.4.6.1
    # (at the time of writing, this is the only data in here)
    object_overrides = {
        "CurrentGameMode": 0x8053C2E0,
        "geGame_ModeDetail": 0x8053C2E4,
        "CurrentStage": 0x8053C2E8,
        "ExitMethod": 0x8053C300,
        "StageTimer": 0x8053C480
    }
    ridersObject1 = RidersObject(object_overrides)

    print(ridersObject1.get_race_state(return_text=True))

    print(ridersObject1.get_current_race_time())