from src.RidersPyTools_KC.Player import Player, DME

if __name__ == "__main__":
    DME.hook()

    # Instantiate player ptr on py side
    player1 = Player(0, 0x80532d80)

    # Set a global lap counter as a lock mechanism
    # Get current lap count (we do this so this counts even if they are past init)
    # MAKE SURE TO TYPECAST TO GET THE INT VALUE
    py_lap_count = int(player1.currentLap)

    print("Lap counter started on lap:", py_lap_count)

    # Use in-game lap count to check updates.
    while True:
        if player1.currentLap > py_lap_count:
            # Increment lap count
            py_lap_count = int(player1.currentLap)
            print("Lap:", player1.currentLap)
        # If player state == startline and the lap counter is greater than 0, reset it.
        if player1.state == 1 and py_lap_count > 0:
            print("Started new race.")
            py_lap_count = 0