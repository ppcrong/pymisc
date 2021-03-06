from loglib import loglib


class filelib:
    slogger = loglib(__name__)

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
            if not file_name or file_name == '':
                filelib.slogger.error('file_name is None or empty!!!')
                ret = False
                break
            if not buf:
                filelib.slogger.error('buf is None!!!')
                ret = False
                break

            try:
                with open(file_name, 'wb') as f:
                    f.write(buf)
                    break
            except IOError as e:
                filelib.slogger.error('Cannot open or write file ({})..'.format(e))
                ret = False
                break
            except TypeError as e:
                filelib.slogger.error('TypeError to write file ({})..'.format(e))
                ret = False
                break

        filelib.slogger.info('ret: {}'.format(ret))
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
            if not file_name or file_name == '':
                filelib.slogger.error('file_name is None or empty!!!')
                break

            try:
                with open(file_name, "rb") as f:
                    buf = f.read()
            except IOError as e:
                filelib.slogger.error('Cannot open or read file ({})..'.format(e))
            except TypeError as e:
                filelib.slogger.error('TypeError to read file ({})..'.format(e))

            break

        return buf


# region [main]
if __name__ == "__main__":
    """
    For console test
    """
# endregion [main]
