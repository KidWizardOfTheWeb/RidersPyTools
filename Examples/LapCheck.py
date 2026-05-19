from src.RidersPyTools_KC.Characters import CHR_ID_TO_NAME
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

    # Hook Dolphin here
    DME.hook()

    # Instantiate player ptr on py side
    player1 = Player(0, TE_PLAYER_PTR)

    # Instantiate the stage timer for 2.4.6.1
    # (at the time of writing, this is the only data in here)
    ridersObject1 = RidersObject(stageTimerAddr=0x8053C480, currentStageAddr=0x8053C2E8)

    # Set a global lap counter as a lock mechanism
    # Get current lap count (we do this so this counts even if they are past init)
    # MAKE SURE TO TYPECAST TO GET THE INT VALUE
    py_lap_count = int(player1.currentLap)

    print("Current stage ID:", STAGE_ID_TO_NAME[int(ridersObject1.currentStage)])

    # Get these values in human-readable form, else give the ID only
    try:
        print("Character:", CHR_ID_TO_NAME[int(player1.character)])
    except KeyError:
        print("Character ID:", int(player1.character))

    try:
        print("Extreme Gear:", GEAR_ID_TO_NAME[int(player1.extremeGear)])
    except KeyError:
        print("Extreme Gear ID:", int(player1.extremeGear))

    try:
        print("Character archetype:", ARCH_ID_TO_NAME[int(player1.characterArchetype)])
    except KeyError:
        print("Character archetype ID:", int(player1.characterArchetype))

    print("\nLap counter started on lap:", py_lap_count)
    print("Current time: {:02d}:{:02d}:{:02d}".format(int(ridersObject1.stageTimer[2]), int(ridersObject1.stageTimer[1]), int(ridersObject1.stageTimer[0])))


    # Use in-game lap count to check updates.
    while True:
        if player1.currentLap > py_lap_count:
            # Show time for lap.
            minutes = int(ridersObject1.stageTimer[2])
            seconds = int(ridersObject1.stageTimer[1])
            milliseconds = int(ridersObject1.stageTimer[0])
            print("Lap time: {:02d}:{:02d}:{:02d}".format(minutes, seconds, milliseconds))

            # Print and save diffs
            current_time = datetime.time(minute=minutes, second=seconds, microsecond=milliseconds)
            diff_time = datetime.time(minute=diff_min, second=diff_sec, microsecond=diff_milli)

            # Yes, the datetime class does NOT allow the difference between two time objects. This is how we have to do it.
            overall_time_diff = datetime.datetime.combine(datetime.date.today(), current_time) - datetime.datetime.combine(datetime.date.today(), diff_time)
            # print("Time diff: " + str(overall_time_diff))
            overall_time_obj = (datetime.datetime.min + overall_time_diff).time()
            print("Time diff: {:02d}:{:02d}:{:02d}".format(overall_time_obj.minute, overall_time_obj.second, overall_time_obj.microsecond))

            # Don't show time diffs on lap 1, to mirror game behavior
            if player1.currentLap != 1:
                diff_min = minutes
                diff_sec = seconds
                diff_milli = milliseconds

            # Increment lap count
            py_lap_count = int(player1.currentLap)
            print("Lap:", player1.currentLap)

        # If player state == startline and the lap counter is greater than 0, reset it.
        if player1.state == 1 and py_lap_count > 0:
            print("Started new race, reset lap count to 0.")
            py_lap_count = 0