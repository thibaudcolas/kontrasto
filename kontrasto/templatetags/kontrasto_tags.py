from django import template

from kontrasto import wcag_2, wcag_3

register = template.Library()


@register.filter(name="dominant_color")
def dominant_color(image):
    return image.get_dominant_color()


@register.filter(name="wcag_2_contrast")
def wcag_2_contrast(image, text_color: str) -> str:
    return wcag_2.wcag2_contrast(image.get_dominant_color(), text_color)

@register.simple_tag(name="wcag_2_contrast_light_or_dark")
def wcag_2_contrast_light_or_dark(image, light_color: str, dark_color: str) -> str:
    dominant = image.get_dominant_color()
    light_contrast = wcag_2.wcag2_contrast(dominant, light_color)
    dark_contrast = wcag_2.wcag2_contrast(dominant, dark_color)
    lighter = light_contrast > dark_contrast
    return {
        "text_color": light_color if lighter else dark_color,
        "text_theme": "light" if lighter else "dark",
        "bg_color": dominant,
        "bg_color_transparent": f"{dominant}aa",
        "bg_theme": "dark" if lighter else "light",
    }


@register.filter(name="wcag_3_contrast")
def wcag_3_contrast(image, text_color: str) -> str:
    return wcag_3.apca_contrast(image.dominant_color, text_color)
