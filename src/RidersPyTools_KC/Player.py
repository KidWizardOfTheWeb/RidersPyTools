"""
CLASS SCHEMA FOR PLAYER

The idea is that we want to read/write to player offsets, so either we do:

Player.read(rings)

or

Player.rings

whatever type we use, the function associated will read byte, halfword, word, or float as needed from
dolphin mem engine, depending on the data from the known player struct

TODO:
We need to find a proper way to associate a data type flag to each offset to make the switch case in the read
function match case properly, then we must add the player pointer to the offset, read that data from dolphin,
and return that.

Writing would be similar, but taking an extra parameter for data to write to the offset given.
"""
import dolphin_memory_engine
from Constants import *
from GameState import *
from src.RidersPyTools_KC.GameState import GAME_VERSION


class Player(object):
    def __init__(self, playerNum):
        match GAME_VERSION:
            case GameVersion.Vanilla:
                self.playerPtr = VANILLA_PLAYER_PTR + (0x1080 * playerNum)
            case GameVersion.DX:
                self.playerPtr = VANILLA_PLAYER_PTR + (0x1080 * playerNum)
            case GameVersion.TE:
                self.playerPtr = TE_PLAYER_PTR + (0x1080 * playerNum)
            case GameVersion.ZG:
                self.playerPtr = ZG_PLAYER_PTR + (0x1120 * playerNum)
            case _:
                pass

        pass

    def read(self, dataOffset):
        # Reads whatever value from dolphin-mem-engine
        # Check datatype associated with dataOffset (either set up as key-value or tuple or something)
        """
        returnValue = None
        match dataOffset:
            case u8:
                dolphin_memory_engine.read_byte(dataOffset)
            case u16:
                ...
            case _:
                print(error)
        :return returnValue:
        """

        def write(self, dataOffset, valueToWrite):
            # Reads whatever value from dolphin-mem-engine
            # Check datatype associated with dataOffset (either set up as key-value or tuple or something)
            """
            match dataOffset:
                case u8:
                    dolphin_memory_engine.write_byte(valueToWrite)
                case u16:
                    ...
                case _:
                    print(error)
            :return returnValue:
        """
        pass

