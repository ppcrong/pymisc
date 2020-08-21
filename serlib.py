import serial

from loglib import loglib


class serlib:
    """
    The library for serial port.
    """

    logger = loglib(__name__)

    def __init__(self, port: str, baudrate: int = 115200):
        self.port = port
        self.serial = None
        try:
            self.serial = serial.Serial(port=port, baudrate=baudrate)
        except serial.serialutil.SerialException as e:
            self.logger.error(e)

    def is_opened(self):
        if self.serial:
            return self.serial.isOpen()
        else:
            self.logger.error('serial is None!!!')
            return False

    def close(self):
        if self.serial:
            self.serial.close()
        else:
            self.logger.error('serial is None!!!')

    # region [with]
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    # endregion [with]

    @staticmethod
    def comports():
        import serial.tools.list_ports as lp
        return lp.comports()

    @staticmethod
    def devices():
        ps = serlib.comports()
        return [p.device for p in ps]

    @staticmethod
    def descriptions():
        ps = serlib.comports()
        return [p.description for p in ps]


if __name__ == "__main__":
    with serlib(port='COM10') as s:
        if not s.is_opened():
            print(f'open {s.port} fail!!!')
        else:
            print(f'open {s.port} ok!!! is_open: {s.is_opened()}')
            s.close()

    ps = serlib.comports()
    print(ps)
    devices = serlib.devices()
    descriptions = serlib.descriptions()
    print(devices)
    print(descriptions)
