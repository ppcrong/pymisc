from filelib import filelib


class Test_filelib:
    test_file = 'test.txt'
    buf = [0x33, 0x34, 0x35, 0x36, 0x37]  # ascii '3', '4', '5', '6', '7'

    def test_file_write_binary(self):
        write_result = filelib.file_write_binary(None, Test_filelib.test_file)
        assert write_result is False

        write_result = filelib.file_write_binary(Test_filelib.buf, None)
        assert write_result is False

        write_result = filelib.file_write_binary(Test_filelib.buf, '')
        assert write_result is False

        write_result = filelib.file_write_binary(Test_filelib.buf, Test_filelib.test_file)
        assert write_result is False

        write_result = filelib.file_write_binary(bytearray(Test_filelib.buf), Test_filelib.test_file)
        assert write_result is True

    def test_file_read_binary(self):
        buf_read = filelib.file_read_binary(None)
        assert buf_read is None

        buf_read = filelib.file_read_binary('')
        assert buf_read is None

        buf_read = filelib.file_read_binary(Test_filelib.test_file)
        print(buf_read)
        assert buf_read == bytes(Test_filelib.buf)

        import os
        if os.path.exists(Test_filelib.test_file):
            os.remove(Test_filelib.test_file)
