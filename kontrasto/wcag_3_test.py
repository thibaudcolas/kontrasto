import unittest

from .wcag_3 import apca_contrast


def to_rgb(hex_code: str):
    h = hex_code.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


class TestUtil(unittest.TestCase):
    def test_apca_contrast(self):
        self.assertEqual(
            apca_contrast(background=to_rgb("#ffffff"), text=to_rgb("#888888")),
            66.89346308821438,
        )
        self.assertEqual(
            apca_contrast(background=to_rgb("#000000"), text=to_rgb("#aaaaaa")),
            -60.438571788907524,
        )
        self.assertEqual(
            apca_contrast(background=to_rgb("#112233"), text=to_rgb("#ddeeff")),
            -98.44863435731266,
        )
        self.assertEqual(
            apca_contrast(background=to_rgb("#223344"), text=to_rgb("#112233")),
            1.276075977788573,
        )
