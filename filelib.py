import enum

from loglib import loglib


class FILE_FMT(enum.IntEnum):
    FOLDER = 0
    IMAGE = FOLDER + 1
    VIDEO = IMAGE + 1
    JSON = VIDEO + 1
    BIN = JSON + 1


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

    @staticmethod
    def get_format(file_name: str):
        from pathlib import Path
        if Path(file_name).is_dir():
            return FILE_FMT.FOLDER
        else:
            import mimetypes
            fmt, _ = mimetypes.guess_type(file_name)
            if fmt.startswith('video'):
                return FILE_FMT.VIDEO
            elif fmt.startswith('image'):
                return FILE_FMT.IMAGE
            elif fmt.endswith('json'):
                return FILE_FMT.JSON
            elif fmt.endswith('octet-stream'):
                return FILE_FMT.BIN


# region [main]
if __name__ == "__main__":
    """
    For console test
    """
# endregion [main]
