import dolphin_memory_engine as DME
from .OffsetAttr import OffsetAttr
from .Constants import *


class GearStats(OffsetAttr):
    def __getattribute__(self, name):
        # This gets our types and offsets (users cannot get these, they are protected from frontend).
        type_to_read = super(GearStats, self).__getattribute__(name)._datatype
        offset_to_read = super(GearStats, self).__getattribute__(name)._offset

        # Check our types, read from game, return value if found
        try:
            value_read = 0
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
            return 0
        return name
    def __setattr__(self, name, value):
        # This gets our types and offsets (users cannot get these, they are protected from frontend).
        type_to_write = super(GearStats, self).__getattribute__(name)._datatype
        offset_to_write = super(GearStats, self).__getattribute__(name)._offset

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
            return
        except RuntimeError as e:
            print("RuntimeError: DME is " + str(e) + ". Failed to write new value.")
        return
    def __init__(self, ptr_start_addr, datatype):
        # Offset attributes:
        # 1. Player Struct offset: 0x0
        # 2. Datatype: u32

        # This will NOT call __setattr__
        super().__init__(0x0, datatype)

        # Do a DME read at the start here of bytes length of struct, then parse that output for the rest here

        # Set attributes here
        super().__setattr__('baseTopSpeed', OffsetAttr(ptr_start_addr + 0x0, f32))
        super().__setattr__('baseAccel', OffsetAttr(ptr_start_addr + 0x4, f32))
        super().__setattr__('topSpeed', OffsetAttr(ptr_start_addr + 0x8, f32))
        super().__setattr__('tier1Accel', OffsetAttr(ptr_start_addr + 0xc, f32))
        super().__setattr__('tier2Accel', OffsetAttr(ptr_start_addr + 0x10, f32))
        super().__setattr__('tier3Accel', OffsetAttr(ptr_start_addr + 0x14, f32))
        super().__setattr__('offroadSpeedCap', OffsetAttr(ptr_start_addr + 0x18, f32))
        super().__setattr__('maxAir', OffsetAttr(ptr_start_addr + 0x1c, s32))
        super().__setattr__('airDrain', OffsetAttr(ptr_start_addr + 0x20, s32))
        super().__setattr__('driftCost', OffsetAttr(ptr_start_addr + 0x24, s32))
        super().__setattr__('boostCost', OffsetAttr(ptr_start_addr + 0x28, s32))
        super().__setattr__('tornadoCost', OffsetAttr(ptr_start_addr + 0x2c, s32))
        super().__setattr__('driftDashSpeed', OffsetAttr(ptr_start_addr + 0x30, f32))
        super().__setattr__('boostSpeed', OffsetAttr(ptr_start_addr + 0x34, f32))
        pass