from ctypes import *

from loglib import loglib


class ctypeslib:

    logger = loglib(__name__)

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

    @staticmethod
    def check_func_exist(dll: CDLL, func_name: str):
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
            ctypeslib.logger.error('dll_khost is None!!!')
            return None

        try:
            return getattr(dll, func_name)
        except AttributeError as err:
            ctypeslib.logger.error(f'{func_name} is None!!!')
            return None
