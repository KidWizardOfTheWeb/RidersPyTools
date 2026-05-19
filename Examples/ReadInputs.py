from src.RidersPyTools_KC.Player import Player, DME
from src.RidersPyTools_KC.include.Constants import *

if __name__ == "__main__":
    DME.hook()

    # Instantiate player ptr on py side
    player1 = Player(0, TE_PLAYER_PTR)

    # Test get
    while True:
        print("left stick horizontal, vertical: {} {}"
              .format(player1.input.leftStickHorizontal,
                      player1.input.leftStickVertical),
              end='\r')