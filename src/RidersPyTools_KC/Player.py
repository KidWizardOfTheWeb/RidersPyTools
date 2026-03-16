"""
CLASS SCHEMA FOR PLAYER

The idea is that we want to read/write to player offsets, so we will use a dict for easy access:

RidersObject["players"] -> accesses the "players" symbol (list of players).

For player ptr data, use a nested dictionary to read/write from offsets. Easiest thing on the eyes, probably:

RidersObject["players"][0]["currentAir"]

Where the layers for the dictionary would have a name and address associated with each.
"Players" is special, due to it being a list

To write:
RidersObject["players"][0]["currentAir"].write(X)

Create a subclass for read/write method

The function associated needs to read byte, halfword, word, or float as needed from
dolphin mem engine, depending on the data from the known player struct

We need to find a proper way to associate a data type flag to each offset to make the switch case in the read
function match case properly, then we must add the player pointer to the offset, read that data from dolphin,
and return that.

Writing would be similar, but taking an extra parameter for data to write to the offset given.
"""
import dolphin_memory_engine as DME
from Constants import *
from GameState import *
from Structs import Controller
from GameState import GAME_VERSION
from Constants import GameIDs
import OffsetAttr
from OffsetAttr import OffsetAttr

class Player(object):
    def __init__(self, playerNum):
        # TODO: If TE, use the map file instead of this for ptr
        match GAME_VERSION:
            # Vanilla based IDs for vanilla, DX, FT
            case GameIDs.SONIC_RIDERS_ID:
                self.playerPtr = VANILLA_PLAYER_PTR + (0x1080 * playerNum)
            case GameIDs.SONIC_RIDERS_DX_ID:
                self.playerPtr = VANILLA_PLAYER_PTR + (0x1080 * playerNum)
            case GameIDs.SONIC_RIDERS_FT_ID:
                self.playerPtr = VANILLA_PLAYER_PTR + (0x1080 * playerNum)

            # TE is special, as the game is a shiftable dol.
            # I'd suggest using the map file to figure out what this is supposed to be,
            # Or having a user enter it manually if no map is passed in.
            case GameIDs.SONIC_RIDERS_TE_ID:
                self.playerPtr = TE_PLAYER_PTR + (0x1080 * playerNum)

            # ZG has dynamic player ptrs, this is not very reliable as of now.
            case GameIDs.SONIC_RIDERS_ZG_ID:
                self.playerPtr = ZG_PLAYER_PTR + (0x1120 * playerNum)

            case _:
                pass
        pass
        # Inputs are always defined on game load, at least for P1.
        # The input ptr is always at the start of the playerPtr struct, so just read word from here and pass the struct ID

        # Controller * input;
        # ptr_start_addr=DME.read_word(self.playerPtr)
        self.input = Controller(0x0, ptr)

        self.tornadoInvulnerabilityTimer = OffsetAttr(0x4, u8)

if __name__ == '__main__':
    # Test init
    new_player_obj = Player(0)

    # Test get
    print(new_player_obj.input.timeSinceLastInput)
    print(new_player_obj.input.port)

    # Test set
    new_player_obj.input.port = 1

    print("Pause")