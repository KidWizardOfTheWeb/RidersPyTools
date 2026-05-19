import dolphin_memory_engine as DME
from .OffsetAttr import OffsetAttr
from .Constants import *

class Controller(OffsetAttr):
    def __getattribute__(self, name):
        # This gets our types and offsets (users cannot get these, they are protected from frontend).
        type_to_read = super(Controller, self).__getattribute__(name)._datatype
        offset_to_read = super(Controller, self).__getattribute__(name)._offset

        # Check our types, read from game, return value if found
        try:
            value_read = 0
            if type_to_read == u8 or type_to_read == s8 or type_to_read == Bool:
                value_read = DME.read_byte(offset_to_read)
            if type_to_read == u16 or type_to_read == s16:
                value_read = DME.read_byte(offset_to_read)
            if type_to_read == u32 or type_to_read == s32:
                value_read = DME.read_word(offset_to_read)
            if type_to_read == f32:
                value_read = DME.read_float(offset_to_read)
            return value_read
        except RuntimeError as e:
            print("RuntimeError: DME is " + str(e) + ". Failed to return value.")
            return 0
        return name

    def __setattr__(self, name, value):
        # This gets our types and offsets (users cannot get these, they are protected from frontend).
        type_to_write = super(Controller, self).__getattribute__(name)._datatype
        offset_to_write = super(Controller, self).__getattribute__(name)._offset

        # Check our types, read from game, return value if found
        try:
            if type_to_write == u8 or type_to_write == s8 or type_to_write == Bool:
                DME.write_byte(offset_to_write, value)
            if type_to_write == u16 or type_to_write == s16:
                DME.write_byte(offset_to_write, value)
            if type_to_write == u32 or type_to_write == s32:
                DME.write_word(offset_to_write, value)
            if type_to_write == f32:
                DME.write_float(offset_to_write, value)
            return
        except RuntimeError as e:
            print("RuntimeError: DME is " + str(e) + ". Failed to write new value.")
        return
    def __init__(self, ptr_start_addr, datatype):
        # Offset attributes:
        # 1. Player Struct offset: 0x0
        # 2. Datatype: ptr
        # 3. ptr address

        # This will NOT call __setattr__
        super().__init__(0x0, datatype, ptr_start_addr)

        # Do a DME read at the start here of bytes length of struct, then parse that output for the rest here

        # Set attributes here
        super().__setattr__('timeSinceLastInput', OffsetAttr(ptr_start_addr + 0x0, u32))
        super().__setattr__('unk4', OffsetAttr(ptr_start_addr + 0x4, u32))
        super().__setattr__('holdFaceButtons', OffsetAttr(ptr_start_addr + 0x8, Flag("Buttons")))
        super().__setattr__('toggleFaceButtons', OffsetAttr(ptr_start_addr + 0xc, Flag("Buttons")))
        super().__setattr__('filler', OffsetAttr(ptr_start_addr + 0x10, fillerData(0x8)))
        super().__setattr__('leftStickHorizontal', OffsetAttr(ptr_start_addr + 0x18, s8))
        super().__setattr__('leftStickVertical', OffsetAttr(ptr_start_addr + 0x19, s8))
        super().__setattr__('filler2', OffsetAttr(ptr_start_addr + 0x1a, fillerData(0x2)))
        super().__setattr__('rightStickHorizontal', OffsetAttr(ptr_start_addr + 0x1c, s8))
        super().__setattr__('rightStickVertical', OffsetAttr(ptr_start_addr + 0x1d, s8))
        super().__setattr__('port', OffsetAttr(ptr_start_addr + 0x1e, u8))
        super().__setattr__('filler3', OffsetAttr(ptr_start_addr + 0x1f, fillerData(0x5)))
        super().__setattr__('initStatus2', OffsetAttr(ptr_start_addr + 0x24, u32))
        super().__setattr__('initStatus', OffsetAttr(ptr_start_addr + 0x28, Bool))
        super().__setattr__('unk29', OffsetAttr(ptr_start_addr + 0x29, Bool))
        super().__setattr__('filler4', OffsetAttr(ptr_start_addr + 0x2a, fillerData(0x6)))
        pass