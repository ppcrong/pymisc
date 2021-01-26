import datetime

import pylink

from loglib import loglib


class pyjlink:

    def __init__(self) -> None:
        super().__init__()
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S.%f')
        self.logger = loglib(f'{__name__}_time{timestamp}')

    def init(self, dll_path: str = None):
        """
        [symptom]
            exception occurred when using dll in dll_path:
            Exception ignored in: <function JLink.__del__ at 0x...>
            OSError: exception: access violation writing 0x...

        [workaround]
            1. first, use installed jlink dll

            2. if not install jlink, then use dll in dll_path
        """
        jlink = None
        try:
            jlink = pylink.JLink()
        except Exception as e:
            self.logger.error(f'{type(e).__name__}!!! {e}')
        finally:
            if not jlink:
                self.logger.info(f'maybe jlink is not installed!!! use dll in dll_path...')
                if dll_path and not dll_path.isspace():
                    try:
                        jlink = pylink.JLink(lib=pylink.jlink.library.Library(dllpath=dll_path))
                    except Exception as e:
                        self.logger.error(f'{type(e).__name__}!!! {e}')
                else:
                    self.logger.info(f'dll_path is invalid or empty!!!')

        if jlink:
            self.logger.info(f'jlink.version: {jlink.version}')
        else:
            self.logger.info(f'jlink is None!!!')
        return jlink

    def deinit(self, jlink: pylink.JLink):
        if jlink:
            jlink.close()

    def connect(self, jlink: pylink.JLink, serial_no: int = None, interface=pylink.enums.JLinkInterfaces.SWD,
                device_xml: str = None, chip_name: str = None, speed: int = 4000):

        ret = False
        while True:
            try:
                self.logger.info(f'num_connected_emulators: {jlink.num_connected_emulators()}')
                jlink.disable_dialog_boxes()

                if serial_no:
                    jlink.open(serial_no=serial_no)
                else:
                    # so far support first jlink connection info
                    info = self.get_first_info(jlink=jlink)
                    if info:
                        # open jlink
                        jlink.open(serial_no=info.SerialNumber)
                        self.logger.i(f'\t\tjlink.firmware_version: {jlink.firmware_version}')
                        self.logger.i(f'\t\tjlink.hardware_version: {jlink.hardware_version}')
                    else:
                        self.logger.error('no jlink!!!')
                        break

                    # set interface (default is SWD)
                    ret = jlink.set_tif(interface)
                    self.logger.i(f'\t\tset_tif ret: {ret}')

                    # set device xml path
                    if device_xml and not device_xml.isspace():
                        ret = jlink.exec_command(f'JLinkDevicesXMLPath = {device_xml}')
                        self.logger.i(f'\t\texec_command (JLinkDevicesXMLPath={device_xml}) ret: {ret}')

                    # connect jlink
                    jlink.connect(chip_name=chip_name, speed=speed)
                    self.logger.i(f'\t\tcore_name: {jlink.core_name()}')

            except Exception as e:
                self.logger.error(f'{type(e).__name__}!!! {e}')
                ret = False
                break

            ret = True
            break

        return ret

    def run_test_ddr(self, jlink: pylink.JLink, mem_base: int, loop: int = 3):

        ret = False
        while True:
            self.logger.info(''.center(50, '#'))
            self.logger.info('# MEMORY TEST START...')
            try:
                test_value_base = 0xFA626000

                if loop < 0:
                    loop = 0

                for j in range(loop):

                    # region [write]
                    self.logger.info(f'# MEMORY TEST WRITE {j + 1}')
                    offset_addr = 0
                    for i in range(5):
                        offset_addr = offset_addr + (0x10 << i)
                        write_value = test_value_base + i
                        self.logger.info(f'\t\toffset_addr: 0x{offset_addr:04X}, write_value: 0x{write_value:08X}')
                        jlink.memory_write32((mem_base + (0x2000000 * j)) + offset_addr, [write_value])
                    # endregion [write]

                    # region [read]
                    self.logger.info(f'# MEMORY TEST READ {j + 1} & VERIFY')
                    offset_addr = 0
                    for i in range(5):
                        offset_addr = offset_addr + (0x10 << i)
                        read = jlink.memory_read32((mem_base + (0x2000000 * j)) + offset_addr, 1)
                        expected_value = test_value_base + i
                        self.logger.info(f'\t\toffset_addr: 0x{offset_addr:04X}, read_value: 0x{read[0]:08X},'
                                         f' expected_value: 0x{expected_value:08X}')
                        if read[0] != expected_value:
                            self.logger.info(f'\t\tVERIFY FAIL!!!')
                            break
                    # endregion [read]

            except Exception as e:
                self.logger.error(f'{type(e).__name__}!!! {e}')
                break
            finally:
                self.logger.info('# MEMORY TEST END...')
                self.logger.info(''.center(50, '#'))

            ret = True
            break

        return ret

    def get_first_info(self, jlink: pylink.JLink):
        info = None
        info_list = jlink.connected_emulators()
        for i, item in enumerate(info_list):
            self.logger.i(f'info[{i}]:')
            self.logger.i(f'\t\tSerial Number: {item.SerialNumber}')
            self.logger.i(f'\t\tConnection: {item.Connection}')

        if len(info_list) > 0:
            info = info_list[0]

        return info

    def simple_test(self, dll_path: str = None, serial_no: int = None, interface=pylink.enums.JLinkInterfaces.SWD,
                    device_xml: str = None, chip_name: str = None, speed: int = 4000, mem_base: int = 0):
        ret = False
        while True:
            jlink = self.init(dll_path=dll_path)
            if not jlink:
                break

            ret = self.connect(jlink=jlink, serial_no=serial_no, interface=interface, device_xml=device_xml,
                               chip_name=chip_name, speed=speed)
            if not ret:
                break

            ret = self.run_test_ddr(jlink=jlink, mem_base=mem_base)
            if not ret:
                break

            break

        self.deinit(jlink=jlink)
        return ret


if __name__ == "__main__":
    """
    For console test
    """
    jlink = pyjlink()
