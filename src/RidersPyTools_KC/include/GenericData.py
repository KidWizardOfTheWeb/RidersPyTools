import dolphin_memory_engine as DME
from .OffsetAttr import OffsetAttr
from .Constants import *

class GenericData(OffsetAttr):
    def __getattribute__(self, name):
        # This gets our types and offsets (users cannot get these, they are protected from frontend).
        type_to_read = vars(super(GenericData, self))['_datatype']
        offset_to_read = vars(super(GenericData, self))['_offset']

        # Check our types, read from game, return value if found
        if 'READ_FROM_DME' in name:
            try:
                value_read = None
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
        return vars(super(GenericData, self))

    def __setattr__(self, name, value):
        # This gets our types and offsets (users cannot get these, they are protected from frontend).
        type_to_write = vars(super(GenericData, self))['_datatype']
        offset_to_write = vars(super(GenericData, self))['_offset']

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

    # Define generics as int comparisons, since most of this is int based.
    def __lt__(self, other):
        return getattr(self, "READ_FROM_DME") < other

    def __le__(self, other):
        return getattr(self, "READ_FROM_DME") <= other

    def __eq__(self, other):
        return getattr(self, "READ_FROM_DME") == other

    def __ne__(self, other):
        return getattr(self, "READ_FROM_DME") != other

    def __gt__(self, other):
        return getattr(self, "READ_FROM_DME") > other

    def __ge__(self, other):
        return getattr(self, "READ_FROM_DME") >= other

    def __int__(self):
        return getattr(self, "READ_FROM_DME")

    def __repr__(self):
        return str(getattr(self, "READ_FROM_DME"))

    def __init__(self, addr, datatype):
        super().__init__(addr, datatype)
        # super().__setattr__(str(name), OffsetAttr(offset=addr, datatype=datatype))
        pass