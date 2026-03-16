"""
This is where a class is defined for each offset, containing the following:
1. Offset
2. Datatype
3. Struct type (if ptr)
"""

class OffsetAttr:
    def __init__(self, offset, datatype, ptr=None, struct=None):
        # REQUIRED TO HAVE BOTH OF THESE
        # self._offset = offset
        super().__setattr__('_offset', offset)
        # self.__dict__["_offset"] = offset
        super().__setattr__('_datatype', datatype)
        # self._datatype = datatype
        # self.__dict__["_datatype"] = datatype
        # Treat this class as a superclass to any other structs that may exist

        # If the attribute is a pointer, set the value it points to here
        if ptr is not None:
            # TODO: Add support for checking where the pointed address leads to
            super().__setattr__('_ptr', ptr)
            # self.__dict__["_ptr"] = ptr
            # self._ptr = ptr
        else:
            pass