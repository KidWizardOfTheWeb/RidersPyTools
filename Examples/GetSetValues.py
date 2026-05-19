from src.RidersPyTools_KC.Player import Player, DME
from src.RidersPyTools_KC.include.Constants import *
import time

if __name__ == "__main__":
    DME.hook()

    # Instantiate player ptr on py side
    player1 = Player(0, 0x80532d80)

    # Test get
    print("Character ID:", player1.character)
    print("Extreme Gear ID:", player1.extremeGear)
    print("Character archetype ID:", player1.characterArchetype)
    print("Current lap:", player1.currentLap)
    print("Player State:", player1.state)

    # Let's adjust their rings!
    print("Changing rings.")
    print("Rings before change:", player1.rings)

    # Set the ring value on the player
    player1.rings = 100
    print("Rings after change:", player1.rings)

    # Play an animation for fun!
    player1.currentAnimationID = 62

    # Do a pause for a second since scripting does not frame match dolphin
    time.sleep(1)

    # Set boost speed
    player1.gearStats[int(player1.level)].boostSpeed = pSpeed(250.0)