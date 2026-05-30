import time

from src.RidersPyTools_KC.Characters import CHR_ID_TO_NAME
from src.RidersPyTools_KC.GameState import RaceState, ExitMethod
from src.RidersPyTools_KC.Gears import GEAR_ID_TO_NAME
from src.RidersPyTools_KC.Stages import STAGE_ID_TO_NAME
from src.RidersPyTools_KC.Archetypes import ARCH_ID_TO_NAME
from src.RidersPyTools_KC.Player import Player, DME
from src.RidersPyTools_KC.RidersObject import RidersObject
from src.RidersPyTools_KC.include.Constants import *

if __name__ == "__main__":
    # Keep some globals for data checks
    diff_min = 0
    diff_sec = 0
    diff_milli = 0

    minutes = 0
    seconds = 0
    centiseconds = 0

    is_reset = False

    restart_count = 0

    LAP_COUNT = 3

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
        if ridersObject1.exitMethod == ExitMethod.Retry and ridersObject1.get_race_state() in {RaceState.Init, RaceState.End} and not is_reset:
            print("-" * 10)
            print("Race restarted.")
            is_reset = True
            py_lap_count = 0
            restart_count += 1
            overall_time_diff = None
            diff_min = 0
            diff_sec = 0
            diff_milli = 0
            print("Restart count:", restart_count)
            print("-"*10)

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

            if current_lap_in_game <= LAP_COUNT:
                print("Lap:", current_lap_in_game)

            if current_lap_in_game == 1:
                minutes = int(ridersObject1.stageTimer[2])
                seconds = int(ridersObject1.stageTimer[1])
                centiseconds = int(ridersObject1.stageTimer[0])
                print("Starting time: {:02d}:{:02d}:{:02d}".format(minutes, seconds, centiseconds))

            # Don't show time diffs on lap 1, to mirror game behavior
            if current_lap_in_game != 1:
                # Always in centiseconds, divide by 100 to get actual seconds.
                # Does not have minutes value, must convert.
                last_lap_time = int(player1.lapTimeList[current_lap_in_game-2]) / 100

                # Divide into minutes and seconds
                minutes, seconds = divmod(last_lap_time, 60)

                # Divide into seconds and centiseconds
                seconds, centiseconds = divmod(seconds, 1)

                # Round centiseconds to 2 places just like in-game
                centiseconds = round(centiseconds, 2) * 100

                # Print here
                print("Lap time: {:02}:{:02}:{:02}".format(int(minutes), int(seconds), int(centiseconds)))

                # Show time for lap.
                minutes = int(ridersObject1.stageTimer[2])
                seconds = int(ridersObject1.stageTimer[1])
                centiseconds = int(ridersObject1.stageTimer[0])

                if current_lap_in_game <= LAP_COUNT:
                    print("Current race time: {:02d}:{:02d}:{:02d}".format(minutes, seconds, centiseconds))

                if current_lap_in_game > LAP_COUNT:
                    # Divide centiseconds to get minutes and seconds
                    final_lap_time = int(player1.lastSplitLapTime) / 100

                    # Divide into minutes and seconds
                    minutes, seconds = divmod(final_lap_time, 60)

                    # Divide into seconds and centiseconds
                    seconds, centiseconds = divmod(seconds, 1)

                    # Round centiseconds to 2 places just like in-game
                    centiseconds = round(centiseconds, 2) * 100

                    # Print here
                    print("Finish time: {:02}:{:02}:{:02}".format(int(minutes), int(seconds), int(centiseconds)))

            time.sleep(0.02)
            print("Speed: {}".format(player1.speedAsInt), "\n")
