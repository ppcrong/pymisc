import sys


class syslib:
    @staticmethod
    def get_platform():
        platforms = {
            'linux': 'Linux',
            'linux1': 'Linux',
            'linux2': 'Linux',
            'darwin': 'OS X',
            'win32': 'Windows'
        }
        if sys.platform not in platforms:
            return sys.platform

        return platforms[sys.platform]

    @staticmethod
    def is_raspberry_pi():
        """
        ref: https://stackoverflow.com/questions/41164147/raspberry-pi-python-detect-os
        """
        try:
            import RPi.GPIO
            ret = True
        except (ImportError, RuntimeError) as e:
            print(e)
            ret = False

        return ret
