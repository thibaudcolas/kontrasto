from willow.registry import registry
from willow.image import Image
from willow.plugins.pillow import PillowImage

from . import wcag_2, wcag_3
from .contrast import get_dominant_color
from .convert import to_hex


def pillow_dominant(image):
    return to_hex(get_dominant_color(image.get_pillow_image()))


# registry.register_operation(PillowImage, "dominant", pillow_dominant)
