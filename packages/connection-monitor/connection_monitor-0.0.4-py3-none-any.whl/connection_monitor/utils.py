from __future__ import annotations


def convert_to_mbit(value: float) -> float:
    """Convert *value* from Bytes to mega-Bytes.

    >>> round(convert_to_mbit(1_000_000.0), 2)
    0.95

    """
    return value / (1024.0**2)
