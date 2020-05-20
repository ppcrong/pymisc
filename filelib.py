from printlib import printlib


class filelib:

    @staticmethod
    def file_write_binary(buf: bytearray, file_name: str):
        """
         write file in binary mode.

        Parameters
        ----------
        buf : bytearray
            write buffer
        file_name : str
            file name

        Returns
        -------
        bool
            write status
        """

        ret = True

        while True:
            printlib.print('file_name: {}'.format(file_name))
            if not file_name or file_name == '':
                printlib.print('file_name is None or empty!!!')
                ret = False
                break;
            if not buf:
                printlib.print('buf is None!!!')
                ret = False
                break;

            try:
                with open(file_name, 'wb') as f:
                    f.write(buf)
                    break;
            except IOError as e:
                printlib.print('Cannot open or write file ({})..'.format(e))
                ret = False
                break;
            except TypeError as e:
                printlib.print('TypeError to write file ({})..'.format(e))
                ret = False
                break;

        printlib.print('ret: {}'.format(ret))
        return ret

    @staticmethod
    def file_read_binary(file_name: str):
        """
         read file in binary mode.

        Parameters
        ----------
        file_name : str
            file name

        Returns
        -------
        bytes
            read buffer
        """

        buf = None

        while True:
            # printlib.print('file_name: {}'.format(file_name))
            if not file_name or file_name == '':
                printlib.print('file_name is None or empty!!!')
                break;

            try:
                with open(file_name, "rb") as f:
                    buf = f.read()
                    # printlib.print('len(buf): {}'.format(len(buf)))
                    break;
            except IOError as e:
                printlib.print('Cannot open or read file ({})..'.format(e))
                break;
            except TypeError as e:
                printlib.print('TypeError to read file ({})..'.format(e))
                break;

        return buf


# region [main]
if __name__ == "__main__":
    """
    For console test
    """

    from filelib import filelib

    write_result = filelib.file_write_binary(None, 'd:/temp/test.txt')
    buf_write = [51, 52, 53]
    write_result = filelib.file_write_binary(buf_write, None)
    write_result = filelib.file_write_binary(buf_write, '')
    write_result = filelib.file_write_binary(buf_write, 'd:/temp/test.txt')
    write_result = filelib.file_write_binary(bytearray(buf_write), 'd:/temp/test.txt')
    buf_read = filelib.file_read_binary(None)
    buf_read = filelib.file_read_binary('')
    buf_read = filelib.file_read_binary('d:/temp/test.txt')
    print(buf_read)
# endregion [main]
