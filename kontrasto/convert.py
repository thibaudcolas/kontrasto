from typing import Sequence

# https://github.com/nathforge/colorops/blob/master/src/colorops/__init__.py
# https://github.com/azaitsev/foreground/blob/master/foreground/__init__.py


def to_rgb_frac(hex_code: str):
    h = hex_code.lstrip("#")
    return tuple(int(h[i : i + 2], 16) / 255 for i in (0, 2, 4))


def to_rgb(hex_code: str):
    h = hex_code.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def to_hex(rgb_tuple: Sequence[int]):
    return "#%02x%02x%02x" % tuple(rgb_tuple)
