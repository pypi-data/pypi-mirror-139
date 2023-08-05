from datetime import datetime
from typing import List

from ws_barcode_scanner.memory_map import MemoryMap
from ws_barcode_scanner.serial_port import SerialPort


class BarcodeScanner:
    __serial_port: SerialPort
    __last_code: bytes
    __last_timestamp: datetime
    memory_map: MemoryMap
    """
    Interface to the device memory
    """

    def __init__(self, serial_port: str):
        self.__serial_port = SerialPort(serial_port)

        self.memory_map = MemoryMap(self.__serial_port)

        self.__last_code = b""
        self.__last_timestamp = datetime.now()

    def save_to_flash(self) -> None:
        """Save the current settings to the persistent flash memory"""
        self.__serial_port.save_to_flash()

    def restore_factory_settings(self) -> None:
        """Restore factory settings"""
        self.__serial_port.restore_factory_settings()

    def query_for_codes(self) -> List[bytes]:
        """Query for scanned codes"""
        response = self.__serial_port.read_all().strip()
        if response:
            codes = response.split(b"\r")
            self.__last_code = codes[-1]
            self.__last_timestamp = datetime.now()
            return codes
        return []

    @property
    def last_code(self) -> bytes:
        """The last scanned barcode"""
        return self.__last_code

    @property
    def last_timestamp(self):
        """The timestamp when the last barcode was scanned (startup time if no code was scanned yet)"""
        return self.__last_timestamp
