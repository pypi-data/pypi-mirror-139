from typing import Tuple, Union, overload

from bitarray import bitarray
from bitarray.util import hex2ba, int2ba

from ws_barcode_scanner.serial_port import SerialPort


class MemoryMap:
    """
    Interface to the device memory
    """

    __serial_port: SerialPort

    def __init__(self, serial_port: SerialPort) -> None:
        self.__serial_port = serial_port

    @overload
    def __getitem__(self, item: Union[int, slice]) -> bitarray:
        ...

    @overload
    def __getitem__(self, item: Tuple[Union[int, slice], int]) -> bool:
        ...

    @overload
    def __getitem__(self, item: Tuple[Union[int, slice], slice]) -> bitarray:
        ...

    def __getitem__(self, key):
        """
        Read data from memory

        Examples
        --------

        >>> # read bytes
        >>> self[0x0000]  # first byte
        bitarray('11001010')
        >>> self[0x0000:0x0002]  # first two bytes
        bitarray('1100101011001010')

        >>> # read bit
        >>> self[0x0000, 0]  # first bit of first byte
        True

        >>> # read bit slices
        >>> self[0x0000, 0:4]  # read first four bits of first byte
        bitarray('1100')
        """
        # self[0] -> bitarray, 8 bits
        if isinstance(key, int):
            return self.__serial_port.read_address(key, 1)

        # self[0:2] -> bitarray, 16 bits
        if isinstance(key, slice):
            key = self.__normalize_slice(key)
            return self.__serial_port.read_address(key.start, key.stop - key.start)

        # self[x, y] -> self[x][y]
        if not isinstance(key, tuple):
            raise IndexError("Only integer, slices, and tuples are allowed")

        if len(key) != 2:
            raise IndexError("Only 2-tuples are supported")

        byte_index, bit_index = key
        data = self[byte_index][bit_index]

        # return single bit as bool
        if isinstance(bit_index, int):
            return bool(data)
        elif isinstance(bit_index, slice):
            return data
        raise TypeError(f"Index not understood: {key}")

    @overload
    def __setitem__(self, key: Union[int, slice], value: Union[bitarray, int, bytes]) -> None:
        ...

    @overload
    def __setitem__(self, key: Tuple[Union[int, slice], int], value: Union[int, bool]) -> None:
        ...

    @overload
    def __setitem__(self, key: Tuple[Union[int, slice], slice], value: Union[bitarray, int, bytes]) -> None:
        ...

    def __setitem__(self, key, value) -> None:
        r"""
        Write data to memory

        Examples
        --------

        >>> # write bytes
        >>> self[0x0000] = bitarray('10100101')  # write `10100101` to first byte
        >>> self[0x0000] = 0b10100101  # same
        >>> self[0x0000] = 165  # same
        >>> self[0x0000] = bytes.fromhex("A5")  # same
        >>> self[0x0000] = b"\xA5"  # same

        >>> # write bit
        >>> self[0x0000, 0] = 0  # set first bit of first byte to 0
        >>> self[0x0000, 0] = False  # same

        >>> # write bit slices
        >>> self[0x0000, -2:] = bitarray('00')  # set last two bits of first byte to `00`
        >>> self[0x0000, -2:] = 0b00  # same
        >>> self[0x0000, -2:] = 0  # same
        """
        if isinstance(key, (int, slice)):
            address, size = self.__key_to_address_and_size(key)
            self.__serial_port.write_to_address(address, size, self.__normalize_data(value, num_bits=size * 8))
            return

        if not isinstance(key, tuple):
            raise IndexError("Only integer, slices, and tuples are allowed")
        if len(key) != 2:
            raise IndexError("Only 2-tuples are supported")
        byte_index, bit_index = key
        original_bytes: bitarray = self[byte_index]

        if isinstance(bit_index, int):
            if isinstance(value, bool) or value == 0 or value == 1:
                original_bytes[bit_index] = value
            else:
                raise ValueError("Can only write True, False, 0, or 1 to a bit address")
        elif isinstance(bit_index, slice):
            original_bytes[bit_index] = self.__normalize_data(value, num_bits=len(original_bytes[bit_index]))
        else:
            raise TypeError(f"Index not understood: {key}")

        address, size = self.__key_to_address_and_size(byte_index)
        self.__serial_port.write_to_address(address, size, original_bytes)

    @staticmethod
    def __normalize_data(data: Union[bitarray, int, bytes], num_bits: int) -> bitarray:
        """
        Normalize the given data into a bitarray

        Parameters
        ----------
        data
            The data
        num_bits
            The number of bits

        Returns
        -------
        The data as bitarray
        """
        # convert data to bitarray
        if isinstance(data, bitarray):
            ba_data = data
        elif isinstance(data, bytes):
            ba_data = hex2ba(data.hex())
        elif isinstance(data, int):
            ba_data = int2ba(data, length=num_bits)
        else:
            raise TypeError(f"Expected bitarray, int, or bytes, got {type(data)} object {data!r}")

        # check size and return
        actual_bits = len(ba_data)
        if actual_bits != num_bits:
            raise ValueError(f"Expected {num_bits} bits of data, {data!r} contains {actual_bits} bits")
        return ba_data

    def __key_to_address_and_size(self, key: Union[int, slice]) -> Tuple[int, int]:
        """
        Convert the byte index (int or slice) to the address of the first byte, and the number of bytes to query

        Parameters
        ----------
        key
            The byte index

        Returns
        -------
        byte_address: int
            The address of the byte to query
        size: int
            The number of bytes to query
        """
        if isinstance(key, int):
            return key, 1
        else:
            key = self.__normalize_slice(key)
            return key.start, key.stop - key.start

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
            key = slice(0, key.stop, key.step)
        return key
