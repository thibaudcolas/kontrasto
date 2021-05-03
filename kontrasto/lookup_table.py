import math
from typing import Any, Dict

# Python port of: https://github.com/Myndex/SAPC-APCA/blob/08a6387df53e93c7825009bd4583872b48687457/images/APCAtable98d12c.png
apca_lookup_table = [
    {
        "contrast": 100,
        "styles": [
            {"size": 24, "weight": 200},
            {"size": 16, "weight": 300},
            {"size": 14, "weight": 400},
        ],
    },
    {
        "contrast": 90,
        "styles": [
            {"size": 30, "weight": 200},
            {"size": 18, "weight": 300},
            {"size": 16, "weight": 400},
            {"size": 14, "weight": 500},
        ],
    },
    {
        "contrast": 80,
        "styles": [
            {"size": 36, "weight": 200},
            {"size": 24, "weight": 300},
            {"size": 18, "weight": 400},
            {"size": 16, "weight": 500},
            {"size": 14, "weight": 600},
        ],
    },
    {
        "contrast": 70,
        "styles": [
            {"size": 48, "weight": 200},
            {"size": 30, "weight": 300},
        ],
    },
    {
        "contrast": 60,
        "styles": [
            {"size": 60, "weight": 200},
            {"size": 36, "weight": 300},
            {"size": 24, "weight": 400},
            {"size": 18, "weight": 500},
            {"size": 16, "weight": 600},
            {"size": 14, "weight": 700},
        ],
    },
    {
        "contrast": 55,
        "styles": [
            {"size": 72, "weight": 200},
            {"size": 48, "weight": 300},
            {"size": 30, "weight": 400},
            {"size": 24, "weight": 500},
            {"size": 18, "weight": 600},
            {"size": 16, "weight": 700},
        ],
    },
    {
        "contrast": 50,
        "styles": [
            {"size": 96, "weight": 200},
            {"size": 60, "weight": 300},
            {"size": 36, "weight": 400},
            {"size": 30, "weight": 500},
            {"size": 24, "weight": 600},
            {"size": 18, "weight": 700},
        ],
    },
    {
        "contrast": 40,
        "styles": [
            {"size": 120, "weight": 200},
            {"size": 72, "weight": 300},
            {"size": 48, "weight": 400},
            {"size": 36, "weight": 500},
            {"size": 30, "weight": 600},
            {"size": 24, "weight": 700},
        ],
    },
]


def get_apca_font_styles(score: float) -> Dict[str, Any]:
    for group in apca_lookup_table:
        if math.fabs(score) > group["contrast"]:
            return group["styles"]

    return []


def get_font_weight(score: float, font_size: int) -> int:
    styles = get_apca_font_styles(score)
    for style in styles:
        if font_size > style["size"]:
            return style["weight"]

    return 700


def get_font_size(score: float, font_weight: int) -> int:
    styles = get_apca_font_styles(score)
    for style in styles:
        if font_weight > style["weight"]:
            return style["size"]

    return 120
