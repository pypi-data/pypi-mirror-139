from typing import List, Tuple, Union, overload

from ws_barcode_scanner.serial_port import SerialPort
from ws_barcode_scanner.utils import bits_to_int, int_to_bits


class MemoryMap:
    """
    Interface to the device memory
    """

    __serial_port: SerialPort

    def __init__(self, serial_port: SerialPort) -> None:
        self.__serial_port = serial_port

    @overload
    def __getitem__(self, item: Union[int, slice]) -> int:
        ...

    @overload
    def __getitem__(self, item: Tuple[Union[int, slice], int]) -> bool:
        ...

    @overload
    def __getitem__(self, item: Tuple[Union[int, slice], slice]) -> int:
        ...

    def __getitem__(self, key):
        """
        Read data from memory

        Examples
        --------

        >>> # read bytes as integers
        >>> self[0x0000]  # first byte
        202
        >>> bin(self[0x0000])  # same number as binary
        '0b11001010'
        >>> bin(self[0x0000:0x0002])  # first two bytes
        '0b1100101011001010'

        >>> # read bit as bool
        >>> self[0x0000, 0]  # first bit of first byte
        True

        >>> # read bit slices as integers
        >>> bin(self[0x0000, 0:4])  # read first four bits of first byte
        '0b1100'
        """
        if isinstance(key, (int, slice)):
            byte_index, bit_index = key, None
        elif isinstance(key, tuple) and len(key) == 2:
            byte_index, bit_index = key
        else:
            raise IndexError(f"Index not understood: {key!r}")

        # read bytes from device
        if isinstance(byte_index, int):  # self[0] -> int, 8 bits
            num_bytes = 1
            byte_data = self.__serial_port.read_address(byte_index, num_bytes)
        elif isinstance(byte_index, slice):  # self[0:2] -> int, 16 bits
            byte_index = self.__normalize_slice(byte_index)
            num_bytes = byte_index.stop - byte_index.start
            byte_data = self.__serial_port.read_address(byte_index.start, num_bytes)
        else:
            raise IndexError(f"Byte index not understood: {byte_index!r}")

        # if full bytes are requested: return them
        if bit_index is None:
            return byte_data

        byte_data_as_bits = int_to_bits(byte_data, n_bits=num_bytes * 8)

        # return requested bits
        if isinstance(bit_index, int):  # self[0, 0] -> bool
            return byte_data_as_bits[bit_index]
        elif isinstance(bit_index, slice):  # self[0, 2:4] -> int, 2 bits
            bit_index = self.__normalize_slice(bit_index)
            return bits_to_int(byte_data_as_bits[bit_index])

        raise IndexError(f"Bit index not understood: {bit_index}")

    @overload
    def __setitem__(self, key: Union[int, slice], value: Union[int, bytes]) -> None:
        ...

    @overload
    def __setitem__(self, key: Tuple[Union[int, slice], int], value: Union[int, bool]) -> None:
        ...

    @overload
    def __setitem__(self, key: Tuple[Union[int, slice], slice], value: Union[int, bytes]) -> None:
        ...

    def __setitem__(self, key, value) -> None:
        r"""
        Write data to memory

        Examples
        --------

        >>> # write bytes
        >>> self[0x0000] = 0b10100101  # write `10100101` to first byte
        >>> self[0x0000] = 165  # same
        >>> self[0x0000] = bytes.fromhex("A5")  # same
        >>> self[0x0000] = b"\xA5"  # same

        >>> # write bit
        >>> self[0x0000, 0] = 0  # set first bit of first byte to 0
        >>> self[0x0000, 0] = False  # same

        >>> # write bit slices
        >>> self[0x0000, -2:] = 0b00  # set last two bits of first byte to `00`
        >>> self[0x0000, -2:] = 0  # same
        """
        if isinstance(key, (int, slice)):
            byte_index, bit_index = key, None
        elif isinstance(key, tuple) and len(key) == 2:
            byte_index, bit_index = key
        else:
            raise TypeError(f"Index not understood: {key!r}")

        if isinstance(byte_index, int):
            address, n_bytes = byte_index, 1
        elif isinstance(byte_index, slice):
            byte_index = self.__normalize_slice(byte_index)
            address, n_bytes = key.start, key.stop - key.start
        else:
            raise IndexError(f"Byte index not understood: {byte_index!r}")

        if isinstance(value, bytes):
            int_value = int.from_bytes(value, byteorder="big")
        elif isinstance(value, int):
            int_value = value
        else:
            raise TypeError("Value must be bytes or integer")

        # write bytes if no bit index is given
        if bit_index is None:
            self.__serial_port.write_to_address(address, n_bytes, int_value)
            return

        # read bytes that have to be partially modified
        bits: List[bool] = list(int_to_bits(self[byte_index], n_bits=n_bytes * 8))

        if isinstance(bit_index, int):
            if isinstance(int_value, bool) or (isinstance(int_value, int) and int_value in (0, 1)):
                bits[bit_index] = bool(int_value)
            else:
                raise ValueError("Can only write True, False, 0, or 1 to a bit address")
        elif isinstance(bit_index, slice):
            bit_index = self.__normalize_slice(bit_index)
            bits[bit_index] = int_to_bits(int_value, n_bits=bit_index.stop - bit_index.start)
        else:
            raise IndexError(f"Bit index not understood: {bit_index}")

        self.__serial_port.write_to_address(address, n_bytes, bits_to_int(bits))

    @staticmethod
    def __normalize_slice(key: slice) -> slice:
        """
        Check and normalize the given byte slice s.t. start is an integer, stop is not None, and step is None

        Parameters
        ----------
        key
            A slice to be used as byte index

        Returns
        -------
        The normalized slice

        Raises
        ------
        IndexError
            If the step was given or stop was not given
        """
        if key.step is not None:
            raise IndexError("Slicing with step != 1 is not supported")
        if key.stop is None:
            raise IndexError("Slicing with open stop is not supported")
        if key.start is None:
            return slice(0, key.stop, None)
        return key
