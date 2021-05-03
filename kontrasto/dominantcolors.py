# -*- coding: utf-8 -*-

# https://github.com/wenmin-wu/dominant-colors-py
__author__ = "wuwenmin1991@gmail.com"

import numpy as np
from numpy import linalg as LA
from PIL import Image
from collections import deque


class ColorNode(object):
    """"""

    def __init__(self):
        self.__mean = None  # the mean of this node
        self.__cov = None  # the covariance of this node
        self.__class_id = None
        self.__left = None
        self.__right = None
        self.__num_pixel = None

    @property
    def mean(self):
        return self.__mean

    @mean.setter
    def mean(self, mean):
        self.__mean = mean

    @property
    def cov(self):
        return self.__cov

    @cov.setter
    def cov(self, cov):
        self.__cov = cov

    @property
    def class_id(self):
        return self.__class_id

    @class_id.setter
    def class_id(self, class_id):
        self.__class_id = class_id

    @property
    def left(self):
        return self.__left

    @left.setter
    def left(self, left):
        self.__left = left

    @property
    def right(self):
        return self.__right

    @right.setter
    def right(self, right):
        self.__right = right

    @property
    def num_pixel(self):
        return self.__num_pixel

    @num_pixel.setter
    def num_pixel(self, num_pixel):
        self.__num_pixel = num_pixel


def rgba2rgb(rgba):
    """
    :param self:
    :param rgba:
    :return:
    """
    background = (255, 255, 255)
    alpha = rgba[..., -1]
    channels = rgba[..., :-1]
    out = np.empty_like(channels)
    for ichan in range(channels.shape[-1]):
        w = alpha / 255.0
        out[..., ichan] = np.clip(
            w * channels[..., ichan] + (1 - w) * background[ichan],
            a_min=0,
            a_max=255,
        )
    out.astype(np.uint8)
    return out


def find_dominant_colors(img_colors, count):
    """
    find dominant colors according to given image colors
    :param img_colors: image colors can either in shape M*N*3 or N*3, the last axis is RGB color
    :param count: number of dominant colors to return
    :return: dominant colors in given number
    """
    colors = img_colors / 255.0
    if len(colors.shape) == 3 and colors.shape[-1] == 3:
        colors = colors.reshape((-1, 3))
    # map each color to the first class id
    classes = np.ones(colors.shape[0], np.int8)
    root = ColorNode()
    root.class_id = 1
    get_class_mean_cov(colors, classes, root)
    for _ in range(count - 1):
        next_node = get_max_eigenvalue_node(root)
        next_class_id = get_next_class_id(root)
        partition_class(colors, classes, next_class_id, next_node)
        get_class_mean_cov(colors, classes, next_node.left)
        get_class_mean_cov(colors, classes, next_node.right)
    return get_dominant_colors(root)


def get_class_mean_cov(colors, classes, node):
    """
    Calculate mean and cov of colors in this class
    """
    curr_node_colors = colors[np.where(classes == node.class_id)]
    node.mean = curr_node_colors.mean(axis=0)
    node.cov = np.cov(curr_node_colors.T)
    node.num_pixel = curr_node_colors.shape[0]


def get_max_eigenvalue_node(curr_node):
    """
    Get the node which has the maximum eigen value of the colors cov
    """
    queue = deque()
    max_eigen = -1
    queue.append(curr_node)
    if not (curr_node.left or curr_node.right):
        return curr_node
    while len(queue):
        node = queue.popleft()
        if node.left and node.right:
            queue.append(node.left)
            queue.append(node.right)
            continue
        eigen_vals, eigen_vecs = LA.eig(node.cov)
        eigen_val = eigen_vals.max()
        if eigen_val > max_eigen:
            max_eigen = eigen_val
            ret = node
    return ret


def get_next_class_id(root):
    max_id = 0
    queue = deque()
    queue.append(root)
    while len(queue):
        curr_node = queue.popleft()
        if curr_node.class_id > max_id:
            max_id = curr_node.class_id
        if curr_node.left:
            queue.append(curr_node.left)
        if curr_node.right:
            queue.append(curr_node.right)
    return max_id + 1


def partition_class(colors, classes, next_id, node):
    class_id = node.class_id
    left_id = next_id
    right_id = next_id + 1
    eigen_vals, eigen_vecs = LA.eig(node.cov)
    eigen_vec = eigen_vecs[eigen_vals.argmax()]
    threshold = np.dot(node.mean, eigen_vec)
    color_indices = np.where(classes == class_id)[0]
    curr_colors = colors[color_indices]
    products = np.dot(curr_colors, eigen_vec)
    left_indices = color_indices[np.where(products <= threshold)[0]]
    right_indices = color_indices[np.where(products > threshold)[0]]
    classes[left_indices] = left_id
    classes[right_indices] = right_id
    node.left = ColorNode()
    node.left.class_id = left_id
    node.right = ColorNode()
    node.right.class_id = right_id


def get_dominant_colors(root):
    dominant_colors = []
    queue = deque()
    queue.append(root)
    while len(queue):
        curr_node = queue.popleft()
        if curr_node.left and curr_node.right:
            queue.append(curr_node.left)
            queue.append(curr_node.right)
            continue
        color = curr_node.mean * 255
        color = np.clip(color, 0, 255)
        color = color.astype(np.uint8)
        dominant_colors.append([curr_node.num_pixel, color.tolist()])
    # it is necessary to sort according to number of pixels in the nodes
    dominant_colors.sort(key=lambda x: x[0], reverse=True)
    return [color[1] for color in dominant_colors]


def get_image_dominant_colors(image_path, num_colors):
    image = Image.open(image_path)
    return get_dominant_colors_for(image, num_colors)


def get_dominant_colors_for(image, num_colors):
    """Get dominant colors from a given pillow Image instance"""
    im_arr = np.asarray(image)
    if image.mode == "RGBA":
        im_arr = rgba2rgb(im_arr)
    return find_dominant_colors(im_arr, num_colors)
