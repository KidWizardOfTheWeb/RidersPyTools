import time

from src.RidersPyTools_KC.Characters import CHR_ID_TO_NAME
from src.RidersPyTools_KC.GameState import RaceState, ExitMethod
from src.RidersPyTools_KC.Gears import GEAR_ID_TO_NAME
from src.RidersPyTools_KC.Stages import STAGE_ID_TO_NAME
from src.RidersPyTools_KC.Archetypes import ARCH_ID_TO_NAME
from src.RidersPyTools_KC.Player import Player, DME
from src.RidersPyTools_KC.RidersObject import RidersObject
from src.RidersPyTools_KC.include.Constants import *

# Python imports
import datetime

if __name__ == "__main__":
    # Keep some globals for data checks
    diff_min = 0
    diff_sec = 0
    diff_milli = 0

    minutes = 0
    seconds = 0
    milliseconds = 0

    is_reset = False

    restart_count = 0

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

    # Set a global lap counter as a lock mechanism
    # Get current lap count (we do this so this counts even if they are past init)
    # MAKE SURE TO TYPECAST TO GET THE INT VALUE
    py_lap_count = int(player1.currentLap)

    print("Current stage:", STAGE_ID_TO_NAME[ridersObject1.currentStage])

    # Get these values in human-readable form, else give the ID only
    try:
        print("Character:", CHR_ID_TO_NAME[player1.character])
    except KeyError:
        print("Character ID:", int(player1.character))

    try:
        print("Extreme Gear:", GEAR_ID_TO_NAME[player1.extremeGear])
    except KeyError:
        print("Extreme Gear ID:", int(player1.extremeGear))

    try:
        print("Character archetype:", ARCH_ID_TO_NAME[player1.characterArchetype])
    except KeyError:
        print("Character archetype ID:", int(player1.characterArchetype))

    print("\nLap counter started on lap:", py_lap_count)
    print("Current time: {:02d}:{:02d}:{:02d}".format(int(ridersObject1.stageTimer[2]), int(ridersObject1.stageTimer[1]), int(ridersObject1.stageTimer[0])))


    # Use in-game lap count to check updates.
    while True:
        # If player state == startline and the lap counter is greater than 0, reset it.
        if ridersObject1.exitMethod == ExitMethod.Retry and ridersObject1.get_race_state() == RaceState.Init and not is_reset:
            print("\nRace restarted.")
            is_reset = True
            py_lap_count = 0
            restart_count += 1
            overall_time_diff = None
            diff_min = 0
            diff_sec = 0
            diff_milli = 0
            print("Restart count:", restart_count, "\n")

        # If you reset and the race is counting down, turn off lock mechanism
        if is_reset and ridersObject1.get_race_state() == RaceState.Countdown:
            # print("Start new race")
            is_reset = False

        if is_reset:
            continue

        current_lap_in_game = int(player1.currentLap)
        if current_lap_in_game > py_lap_count:
            # Increment lap count
            py_lap_count = current_lap_in_game
            print("Lap:", current_lap_in_game)
            # Show time for lap.
            minutes = int(ridersObject1.stageTimer[2])
            seconds = int(ridersObject1.stageTimer[1])
            milliseconds = int(ridersObject1.stageTimer[0])
            if current_lap_in_game == 1:
                print("Starting time: {:02d}:{:02d}:{:02d}".format(minutes, seconds, milliseconds))
            else:
                print("Current race time: {:02d}:{:02d}:{:02d}".format(minutes, seconds, milliseconds))

            # Print and save diffs
            current_time = datetime.time(minute=minutes, second=seconds, microsecond=milliseconds)
            diff_time = datetime.time(minute=diff_min, second=diff_sec, microsecond=diff_milli)

            # Yes, the datetime class does NOT allow the difference between two time objects. This is how we have to do it.
            overall_time_diff = datetime.datetime.combine(datetime.date.today(), current_time) - datetime.datetime.combine(datetime.date.today(), diff_time)
            # print("Time diff: " + str(overall_time_diff))
            overall_time_obj = (datetime.datetime.min + overall_time_diff).time()

            # Don't show time diffs on lap 1, to mirror game behavior
            if current_lap_in_game != 1:
                print("Lap time: {:02d}:{:02d}:{:02d}".format(overall_time_obj.minute, overall_time_obj.second, overall_time_obj.microsecond))
                diff_min = minutes
                diff_sec = seconds
                diff_milli = milliseconds

            time.sleep(0.02)
            print("Speed: {}".format(player1.speedAsInt), "\n")
