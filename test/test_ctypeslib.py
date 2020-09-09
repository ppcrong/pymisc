from ctypes import CDLL

from ctypeslib import ctypeslib


class Test_ctypeslib:
    def test_check_func_exist(self):
        dll_c = CDLL('../asset/libctypes_dll.dll')
        assert ctypeslib.check_func_exist(dll_c, 'test_value')
        assert ctypeslib.check_func_exist(dll_c, 'test_buf')
        assert ctypeslib.check_func_exist(dll_c, 'test_struct_array')
        assert not ctypeslib.check_func_exist(dll_c, 'check_func_exist')
