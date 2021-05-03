from __future__ import division
from typing import Sequence, Union

from .convert import to_rgb_frac

# https://github.com/gsnedders/wcag-contrast-ratio
black_frac = (0.0, 0.0, 0.0)
white_frac = (1.0, 1.0, 1.0)


def wcag2_contrast(
    rgb1: Union[Sequence[int], str], rgb2: Union[Sequence[int], str]
):
    if isinstance(rgb1, str):
        rgb1 = to_rgb_frac(rgb1)
    if isinstance(rgb2, str):
        rgb2 = to_rgb_frac(rgb2)

    for r, g, b in (rgb1, rgb2):
        if not 0.0 <= r <= 1.0:
            raise ValueError("r is out of valid range (0.0 - 1.0)")
        if not 0.0 <= g <= 1.0:
            raise ValueError("g is out of valid range (0.0 - 1.0)")
        if not 0.0 <= b <= 1.0:
            raise ValueError("b is out of valid range (0.0 - 1.0)")

    l1 = _relative_luminance(*rgb1)
    l2 = _relative_luminance(*rgb2)

    if l1 > l2:
        return (l1 + 0.05) / (l2 + 0.05)
    else:
        return (l2 + 0.05) / (l1 + 0.05)


def _relative_luminance(r: float, g: float, b: float):
    r = _linearize(r)
    g = _linearize(g)
    b = _linearize(b)

    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _linearize(v: float):
    if v <= 0.03928:
        return v / 12.92
    else:
        return ((v + 0.055) / 1.055) ** 2.4


def passes_AA(contrast: float, large: bool = False) -> bool:
    if large:
        return contrast >= 3.0
    else:
        return contrast >= 4.5


def passes_AAA(contrast: float, large: bool = False) -> bool:
    if large:
        return contrast >= 4.5
    else:
        return contrast >= 7.0


def format_contrast(score: float) -> str:
    return f"{'{:.2f}'.format(score)}:1"


def format_passes(contrast: float):
    aa = passes_AA(contrast, False)
    aa_large = passes_AA(contrast, True)
    aaa = passes_AAA(contrast, False)
    aaa_large = passes_AAA(contrast, True)
    if aaa:
        return "AAA"

    if aaa_large or aa:
        return "AA, AAA large"

    if aa_large:
        return "AA large only"

    return "fail"
