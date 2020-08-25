import queue
from concurrent.futures.thread import ThreadPoolExecutor

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
        self.bufr = queue.Queue()
        self.bufw = queue.Queue()
        try:
            self.serial = serial.Serial(port=port, baudrate=baudrate, timeout=1, write_timeout=1)
        except serial.serialutil.SerialException as e:
            self.logger.error(e)

    def is_opened(self):
        if self.serial:
            return self.serial.isOpen()
        else:
            self.logger.error('serial is None!!!')
            return False

    def in_waiting(self):
        if self.serial:
            return self.serial.inWaiting()
        else:
            self.logger.error('serial is None!!!')
            return False

    def close(self):
        if self.serial:
            self.serial.close()
        else:
            self.logger.error('serial is None!!!')

    def write_data(self, data: str):
        """
        put write data into queue (write_thread check queue to write)
        """
        self.bufw.put(data)

    def write(self, data: str):
        """
        direct write data
        """
        if self.serial:
            try:
                len_write = self.serial.write(data.encode())
                self.logger.info(f'WRITE len({len_write})')
                self.logger.info(f'WRITE >>> {data}')
            except serial.serialutil.SerialException as e:
                self.logger.error(e)
            except serial.serialutil.SerialTimeoutException as e:
                self.logger.error(e)
        else:
            self.logger.error('serial is None!!!')

    def read(self, size: int):
        """
        direct read data
        """
        ret = None
        if self.serial:
            try:
                raw = self.serial.read(size=size)
                data = raw.decode()
                self.logger.info(f'READ len({len(data)})')
                self.logger.info(f'READ <<<\n{data}')
                ret = data
            except serial.serialutil.SerialException as e:
                self.logger.error(e)
        else:
            self.logger.error('serial is None!!!')
        return ret

    def readline(self):
        ret = None
        if self.serial:
            try:
                raw = self.serial.readline()
                data = raw.decode()
                self.logger.info(f'READ len({len(data)})')
                self.logger.info(f'READ <<< {data}')
                ret = data
            except serial.serialutil.SerialException as e:
                self.logger.error(e)
        else:
            self.logger.error('serial is None!!!')
        return ret

    def start(self):
        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(self.write_thread)
            executor.submit(self.read_thread)
        self.logger.info('all done!!!')

    def stop(self):
        self.close()

    # region [with]
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    # endregion [with]

    # region [thread]
    def read_thread(self):
        """
        keep reading and put data into read buffer
        """
        if not self.serial:
            self.logger.error('serial is None!!!')
            return

        while self.is_opened():
            size = self.in_waiting()
            # self.logger.info(f'size: {size}')
            if size:
                data = self.read(size)
                if data:
                    self.bufr.put(data)

        self.logger.info('EXIT reading...')

    def write_thread(self):
        """
        keep writing when write buffer has data
        """
        if not self.serial:
            self.logger.error('serial is None!!!')
            return

        while self.is_opened():
            if not self.bufw.empty():
                self.write(self.bufw.get(block=True, timeout=1))

        self.logger.info('EXIT writing...')

    # endregion [thread]

    @staticmethod
    def comports():
        import serial.tools.list_ports as lp
        return lp.comports()

    @staticmethod
    def devices():
        ports = serlib.comports()
        return [p.device for p in ports]

    @staticmethod
    def descriptions():
        ports = serlib.comports()
        return [p.description for p in ports]


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
