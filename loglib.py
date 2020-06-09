import datetime
import getpass
import logging
import os

from printlib import printlib


class loglib:
    def __init__(self):
        # get logger
        self.user = getpass.getuser()
        self.logger = logging.getLogger(self.user)
        self.logger.setLevel(logging.DEBUG)
        format = '%(message)s'
        self.formatter = logging.Formatter(format)

        # console handler
        self.consolehandler = logging.StreamHandler()
        self.consolehandler.setFormatter(self.formatter)
        self.logger.addHandler(self.consolehandler)

    @staticmethod
    def get_file_name(prefix='', postfix='', ext='', with_ms=False):
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

    def start_log(self, logfile: str):
        # create folder if not exist
        folder = os.path.dirname(logfile)
        if not os.path.isdir(folder):
            os.mkdir(folder)

        self.filehandler = logging.FileHandler(logfile)
        self.filehandler.setFormatter(self.formatter)
        self.logger.addHandler(self.filehandler)

    # region [just log]
    def d(self, msg=''):
        self.logger.debug(msg)

    def i(self, msg=''):
        self.logger.info(msg)

    def w(self, msg=''):
        self.logger.warning(msg)

    def e(self, msg=''):
        self.logger.error(msg)

    def c(self, msg=''):
        self.logger.critical(msg)

    def l(self, level, msg=''):
        self.logger.log(level, msg)
    # endregion [just log]

    # region [log with caller info]
    def debug(self, msg=''):
        self.logger.debug('D/{} {}'.format(printlib.get_caller_info(2), msg))

    def info(self, msg=''):
        self.logger.info('I/{} {}'.format(printlib.get_caller_info(2), msg))

    def warning(self, msg=''):
        self.logger.warning('W/{} {}'.format(printlib.get_caller_info(2), msg))

    def error(self, msg=''):
        self.logger.error('E/{} {}'.format(printlib.get_caller_info(2), msg))

    def critical(self, msg=''):
        self.logger.critical('C/{} {}'.format(printlib.get_caller_info(2), msg))

    def log(self, level, msg=''):
        self.logger.log(level, '{}/{} {}'.format(logging.getLevelName(level), printlib.get_caller_info(2), msg))
    # endregion [log with caller info]

    def setlevel(self, level):
        self.logger.setLevel(level)

    def disable(self):
        logging.disable(logging.CRITICAL)

    def close_log(self):
        self.logger.removeHandler(self.filehandler)
        self.filehandler.flush()
        self.filehandler.close()

        # self.logger.removeHandler(self.consolehandler)
        # self.consolehandler.flush()
        # self.consolehandler.close()
