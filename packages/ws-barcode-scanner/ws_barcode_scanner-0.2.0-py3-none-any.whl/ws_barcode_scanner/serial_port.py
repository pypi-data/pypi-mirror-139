from functools import lru_cache
from threading import Lock

from serial import Serial

from ws_barcode_scanner.utils import lock_threading_lock


class SerialPort:
    __serial_port: Serial
    __port_lock: Lock
    __timeout: float

    def __init__(self, com_port: str, *, timeout: float = 1) -> None:
        self.__serial_port = Serial(com_port, timeout=timeout, write_timeout=timeout)
        self.__port_lock = Lock()
        self.__timeout = timeout

    def read_all(self) -> bytes:
        """Read all bytes from the input buffer"""
        with lock_threading_lock(self.__port_lock, timeout=self.__timeout):
            return self.__serial_port.read(self.__serial_port.in_waiting)

    def read_address(self, address: int, size: int) -> int:
        """Read `size` bytes from the given memory `address`"""
        hex_address = self.__prepare_address(address)
        hex_size = self.__prepare_size(size)

        expected_response_prefix = f"020000{hex_size}"
        expected_response_length = 6 + size  # header: 2, types: 1, size: 1, crc: 2

        hex_response = self.__communicate(
            f"7E000701{hex_address}{hex_size}", f"020000{hex_size}", expected_response_length
        )

        hex_data = hex_response[len(expected_response_prefix) : -4]  # last 2 bytes (4 hex digits) are crc

        return int(hex_data, base=16)

    def write_to_address(self, address: int, size: int, data: int) -> None:
        """Write the given `size` bytes of `data` to the `address`"""
        hex_size = self.__prepare_size(size)
        hex_address = self.__prepare_address(address)
        hex_data = hex(data)[2:].zfill(2 * size)

        expected_response_prefix = bytes.fromhex("0200000100")
        expected_response_length = len(expected_response_prefix) + 2  # 2 bytes crc suffix

        self.__communicate(f"7E0008{hex_size}{hex_address}{hex_data}", "0200000100", expected_response_length)

    def save_to_flash(self) -> None:
        expected_hex_response = "02000001003331"
        self.__communicate("7E000901000000", expected_hex_response, len(expected_hex_response) // 2)

    def restore_factory_settings(self) -> None:
        expected_hex_response = "02000001003331"
        self.__communicate("7E0009010000FF", expected_hex_response, len(expected_hex_response) // 2)

    def __communicate(self, hex_message: str, expected_hex_prefix: str, expected_bytes: int) -> str:
        """Send `hex_message` to the port and expect `expected_bytes` bytes with the given `expected_hex_prefix`"""
        expected_hex_prefix = expected_hex_prefix.upper()

        message_bytes = bytes.fromhex(hex_message)
        crc_bytes = self.__compute_crc(message_bytes[2:]).to_bytes(length=2, byteorder="big")

        with lock_threading_lock(self.__port_lock, timeout=self.__timeout):
            self.__serial_port.write(message_bytes + crc_bytes)
            raw_response = self.__serial_port.read(expected_bytes)

        hex_response = raw_response.hex().upper()

        if len(raw_response) != expected_bytes:
            raise TimeoutError(f"Expected to receive {expected_bytes} bytes, got '{hex_response}'")

        if not hex_response.startswith(expected_hex_prefix):
            hex_digits_after_prefix = 2 * (len(hex_response) - len(expected_hex_prefix))
            raise ValueError(
                f"Did not receive expected response:"
                f"Got '{hex_response}', expected {expected_hex_prefix}{'X' * hex_digits_after_prefix}"
            )

        return hex_response

    @staticmethod
    def __prepare_size(size: int) -> str:
        """Convert the size to its zero-padded 2-digit hex representation (256 is '00')"""
        if size <= 0 or size > 0xFF:
            raise ValueError(f"Size must be > 0 and <= 256, was {size}")
        return hex(size % 256)[2:].zfill(2)

    @staticmethod
    def __prepare_address(address: int) -> str:
        """Convert the address to its zero-padded 4-digit hex representation"""
        if address < 0 or address >= 0xFF:
            raise ValueError(f"Address must be >= 0 and < 256, was {address}")
        return hex(address)[2:].zfill(4)

    @staticmethod
    @lru_cache()
    def __compute_crc(command: bytes) -> int:
        """Compute the CRC checksum"""

        def _helper_func(c: int) -> int:
            crc = 0
            c <<= 8
            for _ in range(8):
                if (crc ^ c) & 0x8000:
                    crc = (crc << 1) ^ 0x1021
                else:
                    crc <<= 1
                c <<= 1
            return crc

        crc = 0
        for byte in command:
            crc = (crc << 8) ^ _helper_func(((crc >> 8) ^ (0xFF & byte)) & 0xFF)
            crc &= 0xFFFF

        return crc
