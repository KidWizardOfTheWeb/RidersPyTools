import dolphin_memory_engine
from OffsetAttr import OffsetAttr
from Constants import *

class Controller(OffsetAttr):
    def __getattribute__(self, item):
        # TODO: Implement DME read calls here
        return item
    # def __getattr__(self, name):
    #     # TODO: Implement DME read calls here
    #     return 0
    def __setattr__(self, key, value):
        # TODO: Implement DME write calls here
        return 0
    def __init__(self, ptr_start_addr, datatype):
        # Offset attributes:
        # 1. Player Struct offset: 0x0
        # 2. Datatype: ptr
        # 3. ptr address

        # This will NOT call __setattr__
        super().__init__(0x0, datatype, ptr_start_addr)

        # Do a DME read at the start here of bytes length of struct, then parse that output for the rest here

        # Create a list of lists and loop __setattr__
        # TODO: fix all offsets to proper value with script.
        super().__setattr__('timeSinceLastInput', OffsetAttr(ptr_start_addr + 0, u32, None))
        super().__setattr__('unk4', OffsetAttr(ptr_start_addr + 4, u32, None))
        super().__setattr__('holdFaceButtons', OffsetAttr(ptr_start_addr + 8, u32, None)) # Flag<Buttons>
        super().__setattr__('toggleFaceButtons', OffsetAttr(ptr_start_addr + 12, u32, None)) # Flag<Buttons>
        # super().__setattr__('filler', OffsetAttr(ptr_start_addr + 16, fillerData<0x8>, None))
        super().__setattr__('leftStickHorizontal', OffsetAttr(ptr_start_addr + 20, s8, None))
        super().__setattr__('leftStickVertical', OffsetAttr(ptr_start_addr + 24, s8, None))
        # super().__setattr__('filler2', OffsetAttr(ptr_start_addr + 28, fillerData<0x2>, None))
        super().__setattr__('rightStickHorizontal', OffsetAttr(ptr_start_addr + 32, s8, None))
        super().__setattr__('rightStickVertical', OffsetAttr(ptr_start_addr + 36, s8, None))

        # Correct attribute setting without triggering __setattr__
        super().__setattr__('port', OffsetAttr(ptr_start_addr + 40, u8, None))

        # super().__setattr__('filler3', OffsetAttr(ptr_start_addr + 44, fillerData<0x5>, None))
        super().__setattr__('initStatus2', OffsetAttr(ptr_start_addr + 48, u32, None))
        super().__setattr__('initStatus', OffsetAttr(ptr_start_addr + 52, bool, None))
        super().__setattr__('unk29', OffsetAttr(ptr_start_addr + 56, bool, None))
        # super().__setattr__('filler4', OffsetAttr(ptr_start_addr + 60, fillerData<0x6>, None))
        pass
