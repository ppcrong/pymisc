import datetime
import logging
import os
import sys

from printlib import printlib


class loglib:
    def __init__(self, module: str = None):
        # get logger per module
        self.logger = logging.getLogger(module)
        self.logger.setLevel(logging.DEBUG)
        format = '%(message)s'
        self.formatter = logging.Formatter(format)

        # console handler init
        self.consolehandler = logging.StreamHandler(sys.stdout)
        self.consolehandler.setFormatter(self.formatter)
        self.logger.addHandler(self.consolehandler)
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

    def start_log(self, logfile: str):
        # create folder if not exist
        folder = os.path.dirname(logfile)
        if not os.path.isdir(folder):
            import pathlib
            pathlib.Path(folder).mkdir(parents=True, exist_ok=True)

        # file handler
        self.filehandler = logging.FileHandler(logfile)
        self.filehandler.setFormatter(self.formatter)
        self.logger.addHandler(self.filehandler)

    # region [just log]
    def d(self, msg: str = ''):
        self.logger.debug(msg)

    def i(self, msg: str = ''):
        self.logger.info(msg)

    def w(self, msg: str = ''):
        self.logger.warning(msg)

    def e(self, msg: str = ''):
        self.logger.error(msg)

    def c(self, msg: str = ''):
        self.logger.critical(msg)

    def l(self, level: int, msg: str = ''):
        self.logger.log(level, msg)

    # endregion [just log]

    # region [log with caller info]
    def debug(self, msg: str = ''):
        self.logger.debug('D/{} {}'.format(printlib.get_caller_info(2), msg))

    def info(self, msg: str = ''):
        self.logger.info('I/{} {}'.format(printlib.get_caller_info(2), msg))

    def warning(self, msg: str = ''):
        self.logger.warning('W/{} {}'.format(printlib.get_caller_info(2), msg))

    def error(self, msg: str = ''):
        self.logger.error('E/{} {}'.format(printlib.get_caller_info(2), msg))

    def critical(self, msg: str = ''):
        self.logger.critical('C/{} {}'.format(printlib.get_caller_info(2), msg))

    def log(self, level: int, msg: str = ''):
        self.logger.log(level, '{}/{} {}'.format(logging.getLevelName(level), printlib.get_caller_info(2), msg))

    # endregion [log with caller info]

    def setlevel(self, level: int):
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


# region [main]
if __name__ == "__main__":
    """
    For console test
    """

    from loglib import loglib

    logger = loglib('loglib_test')
    logger.info('info')
    logger.debug('debug')
    logger.i('info')
    logger.d('debug')

    # test log file
    logger = loglib('loglib_file')
    log_folder = 'logs'
    log_file = loglib.get_file_name(prefix='loglib', postfix='loglib', ext='log')
    logger.start_log(os.path.join(log_folder, log_file))
    logger.info('info')
    logger.debug('debug')
    logger.i('info')
    logger.d('debug')
    logger.close_log()

# endregion [main]
