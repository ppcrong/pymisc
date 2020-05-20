from ctypes import *


class ctypeslib:

    # region [https://tinyurl.com/y933rm4s]
    @staticmethod
    def convert_bytes_to_struct(byte, st):
        # sizoef(st) == sizeof(byte)
        memmove(addressof(st), byte, sizeof(st))

    @staticmethod
    def convert_struct_to_bytes(st):
        buffer = create_string_buffer(sizeof(st))
        memmove(buffer, addressof(st), sizeof(st))
        return buffer.raw

    @staticmethod
    def convert_int_to_bytes(number, size, byteorder):
        return number.to_bytes(size, byteorder)
    # endregion [https://tinyurl.com/y933rm4s]
