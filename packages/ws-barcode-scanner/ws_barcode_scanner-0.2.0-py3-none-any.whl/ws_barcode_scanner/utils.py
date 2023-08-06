from contextlib import contextmanager
from threading import Lock
from typing import Iterator, Sequence, Tuple


@contextmanager
def lock_threading_lock(lock: Lock, *, timeout: float) -> Iterator[None]:
    """Context manager for using a `threading.lock` with a timeout"""
    if not timeout > 0:
        raise ValueError("Timeout must be positive")

    if not lock.acquire(timeout=timeout):
        raise TimeoutError(f"Could not acquire lock after {timeout} seconds")

    try:
        yield
    finally:
        lock.release()


def int_to_bits(num: int, n_bits: int) -> Tuple[bool, ...]:
    """
    Convert an integer to its bit representation.

    Examples
    --------

    >>> int_to_bits(3, 2)
    (True, True)
    >>> int_to_bits(0xF1, 8)
    (True, True, True, True, False, False, False, True)
    """
    max_num_representable_by_n_bits = 2**n_bits - 1
    if num > max_num_representable_by_n_bits:
        raise ValueError(f"{n_bits} can only represent numbers <= {max_num_representable_by_n_bits}, got {num}")
    return tuple(bool(num & (2 ** (n_bits - i - 1))) for i in range(n_bits))


def bits_to_int(bits: Sequence[bool]) -> int:
    return sum(bit * 2**i for (i, bit) in enumerate(bits[::-1]))
