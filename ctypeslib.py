import ctypes

from loglib import loglib


class ctypeslib:
    slogger = loglib(__name__)

    # region [https://tinyurl.com/y933rm4s]
    @staticmethod
    def convert_bytes_to_struct(byte, st):
        # sizoef(st) == sizeof(byte)
        ctypes.memmove(ctypes.addressof(st), byte, ctypes.sizeof(st))

    @staticmethod
    def convert_struct_to_bytes(st):
        buffer = ctypes.create_string_buffer(ctypes.sizeof(st))
        ctypes.memmove(buffer, ctypes.addressof(st), ctypes.sizeof(st))
        return buffer.raw

    @staticmethod
    def convert_int_to_bytes(number, size, byteorder):
        return number.to_bytes(size, byteorder)

    # endregion [https://tinyurl.com/y933rm4s]

    @staticmethod
    def check_func_exist(dll: ctypes.CDLL, func_name: str):
        """
        Check function existence.

        Parameters
        ----------
        dll : CDLL
            dll for check
        func_name : str
            function name

        Returns
        -------
        object
            function object or None if not exist
        """

        if not dll:
            ctypeslib.slogger.error('dll is None!!!')
            return None

        try:
            return getattr(dll, func_name)
        except AttributeError as err:
            ctypeslib.slogger.error(f'{func_name} is None!!!')
            return None
