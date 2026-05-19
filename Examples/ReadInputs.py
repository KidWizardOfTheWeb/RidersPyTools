from src.RidersPyTools_KC.Player import Player, DME

if __name__ == "__main__":
    DME.hook()

    # Instantiate player ptr on py side
    player1 = Player(0, 0x80532d80)

    # Test get
    while True:
        print("left stick horizontal, vertical: {} {}"
              .format(player1.input.leftStickHorizontal,
                      player1.input.leftStickVertical),
              end='\r')