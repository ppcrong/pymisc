import datetime
import logging
import os
import sys

from printlib import printlib


class loglib:
    def __init__(self, module: str = None):
        # get logger per module
        self.module = module
        self.logger = logging.getLogger(module)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(message)s')

        # console handler init
        self.consolehandler = None
        # file handler init
        self.filehandler = None

    @staticmethod
    def get_file_name(prefix: str = '', postfix: str = '', ext: str = '', with_ms: bool = False):
        if with_ms:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S.%f')[:-3]
        else:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

        filename = ''

        if prefix:
            filename += prefix + '_' + timestamp
        else:
            filename = timestamp

        if postfix:
            filename += '_' + postfix

        if ext:
            filename += '.' + ext

        return filename

    def _init_console(log):
        """
        init_console decorator
        """
        def func(self, msg: str = ''):
            self.init_console()
            log(self, msg)
        return func

    def init_console(self):
        if not self.consolehandler:
            # print(f' init console {self.module} '.center(100, '^'))
            self.start_console()

    def start_console(self):
        """
        [symptom]
            1. a class, for example (class test:) has self.logger = loglib(__name__) in __init__
            2. create test class instance like: t1 = test()
            3. deepcopy t1 to t2 => t2 = copy.deepcopy(t1)
            4. exception occurred => TypeError: cannot pickle '_thread.RLock' object
        [root cause] loglib.__init__ has logging.StreamHandler(sys.stdout)
        [solution] init console handler out of __init__
        """
        self.consolehandler = logging.StreamHandler(sys.stdout)
        self.consolehandler.setFormatter(self.formatter)
        self.logger.addHandler(self.consolehandler)

    def start_log(self, logfile: str):
        self.create_parent_folder(logfile)

        # file handler
        self.filehandler = logging.FileHandler(logfile)
        self.filehandler.setFormatter(self.formatter)
        self.logger.addHandler(self.filehandler)

    @staticmethod
    def create_parent_folder(file_path: str):
        """
        create file's parent folder if not exist
        """
        folder = os.path.dirname(file_path)
        if not os.path.exists(folder):
            import pathlib
            pathlib.Path(folder).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def create_folder(folder_path: str):
        """
        create folder if not exist
        """
        if not os.path.exists(folder_path):
            import pathlib
            pathlib.Path(folder_path).mkdir(parents=True, exist_ok=True)

    # region [just log]
    @_init_console
    def d(self, msg: str = ''):
        self.logger.debug(msg)

    @_init_console
    def i(self, msg: str = ''):
        self.logger.info(msg)

    @_init_console
    def w(self, msg: str = ''):
        self.logger.warning(msg)

    @_init_console
    def e(self, msg: str = ''):
        self.logger.error(msg)

    @_init_console
    def c(self, msg: str = ''):
        self.logger.critical(msg)

    @_init_console
    def l(self, level: int, msg: str = ''):
        self.logger.log(level, msg)

    # endregion [just log]

    # region [log with time and level]
    @_init_console
    def d1(self, msg: str = ''):
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S.%f')[:-3]
        self.logger.debug(f'D/{timestamp} {msg}')

    @_init_console
    def i1(self, msg: str = ''):
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S.%f')[:-3]
        self.logger.debug(f'I/{timestamp} {msg}')

    @_init_console
    def w1(self, msg: str = ''):
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S.%f')[:-3]
        self.logger.debug(f'W/{timestamp} {msg}')

    @_init_console
    def e1(self, msg: str = ''):
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S.%f')[:-3]
        self.logger.debug(f'E/{timestamp} {msg}')

    @_init_console
    def c1(self, msg: str = ''):
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S.%f')[:-3]
        self.logger.debug(f'C/{timestamp} {msg}')

    @_init_console
    def l1(self, level: int, msg: str = ''):
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S.%f')[:-3]
        self.logger.log(level, f'{logging.getLevelName(level)}/{timestamp} {msg}')

    # endregion [log with time and level]

    # region [log with caller info]
    @_init_console
    def debug(self, msg: str = ''):
        self.logger.debug('D/{} {}'.format(printlib.get_caller_info(3), msg))

    @_init_console
    def info(self, msg: str = ''):
        self.logger.info('I/{} {}'.format(printlib.get_caller_info(3), msg))

    @_init_console
    def warning(self, msg: str = ''):
        self.logger.warning('W/{} {}'.format(printlib.get_caller_info(3), msg))

    @_init_console
    def error(self, msg: str = ''):
        self.logger.error('E/{} {}'.format(printlib.get_caller_info(3), msg))

    @_init_console
    def critical(self, msg: str = ''):
        self.logger.critical('C/{} {}'.format(printlib.get_caller_info(3), msg))

    @_init_console
    def log(self, level: int, msg: str = ''):
        self.logger.log(level, '{}/{} {}'.format(logging.getLevelName(level), printlib.get_caller_info(3), msg))

    # endregion [log with caller info]

    def setlevel(self, level: int):
        self.logger.setLevel(level)

    def disable(self):
        logging.disable(logging.CRITICAL)

    def close_console(self):
        self.logger.removeHandler(self.consolehandler)
        self.consolehandler.flush()
        self.consolehandler.close()
        self.consolehandler = None

    def close_log(self):
        self.logger.removeHandler(self.filehandler)
        self.filehandler.flush()
        self.filehandler.close()
        self.filehandler = None


# region [main]
if __name__ == "__main__":
    """
    For console test
    """
# endregion [main]
