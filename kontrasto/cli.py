import argparse
import json
from pathlib import Path
from typing import Iterable

from willow.registry import registry
from willow.image import Image
from willow.plugins.pillow import PillowImage

from . import __version__, wcag_2, wcag_3
from .contrast import get_dominant_color
from .convert import to_hex


def pillow_dominant(image):
    return to_hex(get_dominant_color(image.get_pillow_image()))


registry.register_operation(PillowImage, "dominant", pillow_dominant)


def get_whocanuse_url(b: str, c: str = "", f: str = 16, s: bool = False) -> str:
    return f"https://whocanuse.com/?b={b.lstrip('#')}&c={c.lstrip('#')}&f={f}{'&s=b' if s else ''}"


def get_apca_url(bg: str, txt: str = "") -> str:
    return f"https://www.myndex.com/APCA/?BG={bg.lstrip('#')}&TXT={txt.lstrip('#')}"  # &DEV=98G4g&BUF=APCA-G


def get_whocanuse_urls(b: str, c: str, styles: Iterable[Iterable[int]]) -> str:
    return "\n".join(
        [get_whocanuse_url(b, c, style[0], style[1] >= 600) for style in styles]
    )


def main() -> None:
    p = argparse.ArgumentParser()
    p.version = __version__
    p.add_argument("Path", metavar="path", type=str, help="image file path")
    p.add_argument(
        "--text",
        action="store",
        type=str,
        help="hex code color of the text foreground",
    )
    p.add_argument(
        "--weights",
        action="store",
        type=str,
        help="list of allowed weights",
        default="400,500,600,700",
    )
    p.add_argument(
        "--sizes",
        action="store",
        type=str,
        help="list of allowed sizes",
        default="16,18,24",
    )
    p.add_argument("--verbose", action="store_true", help="verbose output")
    p.add_argument("--version", action="version")

    # Execute parse_args()
    args = p.parse_args()

    source = Path(args.Path)
    weights = sorted(json.loads(f"[{args.weights}]"))
    sizes = sorted(json.loads(f"[{args.sizes}]"))

    if not args.Path or not source:
        return

    with open(source, "rb") as f:
        i = Image.open(f)

        dominant_hex = i.dominant()
        contrast_2_black = wcag_2.wcag2_contrast(
            wcag_2.black_frac, dominant_hex
        )
        contrast_2_white = wcag_2.wcag2_contrast(
            wcag_2.white_frac, dominant_hex
        )

        if args.text:
            contrast_2_text = wcag_2.wcag2_contrast(args.text, dominant_hex)

        print(
            f"Dominant color: {dominant_hex} ({get_whocanuse_url(dominant_hex)})"
        )
        print(
            f"WCAG 2 contrast black: {wcag_2.format_contrast(contrast_2_black)} ({wcag_2.format_passes(contrast_2_black)}, {get_whocanuse_url(dominant_hex, '000000')})"
        )
        print(
            f"WCAG 2 contrast white: {wcag_2.format_contrast(contrast_2_white)} ({wcag_2.format_passes(contrast_2_white)}, {get_whocanuse_url(dominant_hex, 'ffffff')})"
        )

        if contrast_2_text:
            print(
                f"WCAG 2 contrast text color: {wcag_2.format_contrast(contrast_2_text)} ({wcag_2.format_passes(contrast_2_text)}, {get_whocanuse_url(dominant_hex, args.text)})"
            )

        contrast_3_black = wcag_3.apca_contrast(dominant_hex, "#000000")
        styles_black = wcag_3.get_font_styles(contrast_3_black, weights, sizes)
        contrast_3_white = wcag_3.apca_contrast(dominant_hex, "#ffffff")
        styles_white = wcag_3.get_font_styles(contrast_3_white, weights, sizes)

        if args.text:
            contrast_3_text = wcag_3.apca_contrast(dominant_hex, args.text)
            styles_text = wcag_3.get_font_styles(
                contrast_3_text, weights, sizes
            )

        print(
            f"WCAG 3 contrast black: {wcag_3.format_contrast(contrast_3_black)}"
        )
        if styles_black:
            print(styles_black)
            print(get_apca_url(dominant_hex, "000000"))
            print(get_whocanuse_urls(dominant_hex, "000000", styles_black))
        else:
            print(get_whocanuse_url(dominant_hex, "000000"))

        print(
            f"WCAG 3 contrast white: {wcag_3.format_contrast(contrast_3_white)}"
        )
        if styles_white:
            print(styles_white)
            print(get_apca_url(dominant_hex, "ffffff"))
            print(get_whocanuse_urls(dominant_hex, "ffffff", styles_white))
        else:
            print(get_whocanuse_url(dominant_hex, "ffffff"))

        if contrast_3_text:
            print(
                f"WCAG 3 contrast text color: {wcag_3.format_contrast(contrast_3_text)}"
            )
            if styles_text:
                print(styles_text)
                print(get_apca_url(dominant_hex, args.text))
                print(get_whocanuse_urls(dominant_hex, args.text, styles_text))
            else:
                print(get_whocanuse_url(dominant_hex, args.text))


if __name__ == "__main__":
    main()
