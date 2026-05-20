"""
Contains all memory addresses from map/vanilla addresses fallback
"""

import dolphin_memory_engine as DME
from .include.Controller import Controller
from .include.GenericData import GenericData
from .include.GearStats import GearStats
from .include.Constants import *
from .GameState import GAME_VERSION
INIT_STATE = True
class RidersObject:
    def __getattr__(self, name):
        global INIT_STATE

        if INIT_STATE:
            return None

        # This gets our types and offsets (users cannot get these, they are protected from frontend).
        type_to_read = vars(self.__getattribute__(name))["_datatype"]
        offset_to_read = vars(self.__getattribute__(name))["_offset"]

        # Check our types, read from game, return value if found
        if 'READ_FROM_DME' in name:
            try:
                value_read = None
                if type_to_read == u8 or type_to_read == s8 or type_to_read == Bool:
                    value_read = DME.read_byte(offset_to_read)
                if type_to_read == u16 or type_to_read == s16:
                    value_read = DME.read_byte(offset_to_read)
                if type_to_read == u32 or type_to_read == s32 or type_to_read == vu32:
                    value_read = DME.read_word(offset_to_read)
                if type_to_read == f32:
                    value_read = DME.read_float(offset_to_read)
                return value_read
            except RuntimeError as e:
                print("RuntimeError: DME is " + str(e) + ". Failed to return value.")
        return vars(self.__getattribute__(name))
    def __setattr__(self, name, value):
        global INIT_STATE

        # On startup, this allows everything to be assigned to the player object.
        # We NEED this for init ONLY.
        # Once every struct variable is done, SET INIT_STATE = False.
        # Once that is done, this will retrieve data from DME instead of setting the attribute's value.
        if INIT_STATE:
            super().__setattr__(name, value)
            return
        # Use this function for GenericData value assignment that isn't setting equal to a new object instance (that's handled in their own classes)

        # This gets our types and offsets (users cannot get these, they are protected from frontend).
        # check_DME_value = vars(self.__getattribute__(name))
        type_to_write = vars(self.__getattribute__(name))["_datatype"]
        offset_to_write = vars(self.__getattribute__(name))["_offset"]

        # Check our types, read from game, return value if found
        try:
            if type_to_write == u8 or type_to_write == s8 or type_to_write == Bool:
                DME.write_byte(offset_to_write, value)
            if type_to_write == u16 or type_to_write == s16:
                DME.write_byte(offset_to_write, value)
            if type_to_write == u32 or type_to_write == s32 or type_to_write == vu32:
                DME.write_word(offset_to_write, value)
            if type_to_write == f32:
                DME.write_float(offset_to_write, value)
        except RuntimeError as e:
            print("RuntimeError: DME is " + str(e) + ". Failed to write new value.")
        return
    def __init__(self, stageTimerAddr=None, currentStageAddr=None):
        global INIT_STATE
        INIT_STATE = True
        # Find a way to define literally EVERY SYMBOL here.
        # Not easy, but most are defined. Some are custom with pointers and structs. Good luck.

        # This is a hack that allows me to change where the addresses are.
        # This makes it easier to find while we're testing TE.
        # If no address found, use vanilla.
        # If you want this for TE, send in stageTimerAddr 0x8053C480
        # TE 2.4.6.1 currentStageAddr 0x8053C2E8
        if not stageTimerAddr:
            stageTimerAddr = 0x80612b40
        if not currentStageAddr:
            currentStageAddr = 0x806129A8
        self.stageTimer = [GenericData(stageTimerAddr, u8), GenericData(stageTimerAddr + 0x1, u8),
                           GenericData(stageTimerAddr + 0x2, u8)]
        self.currentStage = GenericData(currentStageAddr, vu32)

        INIT_STATE = False
        pass