"""Processing for the image."""

from typing import Tuple

import cv2
import numpy as np


def resize(img: np.ndarray, output_size: Tuple[int, int], padding: bool = True) -> np.ndarray:
    """Resize the image.

    resize the image with padding or crop

    Args:
        img (numpy.ndarray): OpenCV image
        output_size (Tuple[int, int]): size of the output image
        padding (bool): whether to perform padding or not

    Returns:
        numpy.ndarray: OpenCV image

    """
    x = img.shape[1]
    y = img.shape[0]
    out_x, out_y = output_size
    in_rate = x / y
    out_rate = out_x / out_y
    if padding:
        if in_rate == out_rate:
            resized = np.copy(img)
        elif in_rate >= out_rate:
            resized_y = int(x / out_rate)
            start = (resized_y - y) // 2
            end = (resized_y + y) // 2
            resized = cv2.resize(np.zeros((1, 1, 3), np.uint8), (x, resized_y))
            resized[start:end, :] = img
        else:
            resize_x = int(y * out_rate)
            start = (resize_x - x) // 2
            end = (resize_x + x) // 2
            resized = cv2.resize(np.zeros((1, 1, 3), np.uint8), (resize_x, y))
            resized[:, start:end] = img
    else:
        if in_rate == out_rate:
            resized = np.copy(img)
        elif in_rate >= out_rate:
            resize_x = int(y * out_rate)
            d = x - resize_x
            gap_x = d // 2
            resized = img[:, gap_x : gap_x + resize_x]
        else:
            resize_y = int(x / out_rate)
            d = y - resize_y
            gap_y = d // 2
            resized = img[gap_y : gap_y + resize_y, :]
    resized = cv2.resize(resized, dsize=output_size)

    return resized
