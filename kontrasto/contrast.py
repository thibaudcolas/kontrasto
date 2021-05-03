# https://github.com/wenmin-wu/dominant-colors-py
from .dominantcolors import rgba2rgb, find_dominant_colors
import numpy as np


def get_dominant_colors_for(pillow_image, num_colors):
    """Get dominant colors from a given pillow Image instance"""
    im_arr = np.asarray(pillow_image)
    if pillow_image.mode == "RGBA":
        im_arr = rgba2rgb(im_arr)
    return find_dominant_colors(im_arr, num_colors)


def get_dominant_color(pillow_image):
    dominant_colors = get_dominant_colors_for(pillow_image, num_colors=1)
    return dominant_colors[0]
