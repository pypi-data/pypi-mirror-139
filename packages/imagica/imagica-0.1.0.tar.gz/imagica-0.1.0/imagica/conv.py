"""Convert the image format."""

import numpy as np
from PIL import Image


def cv2pil(img: np.ndarray) -> Image.Image:
    """Convert OpenCV->PIL.

    convert the format from OpenCV to PIL

    Args:
        img (numpy.ndarray): OpenCV image

    Returns:
        PIL.Image.Image: PIL image

    """
    converted = img.copy()
    if converted.ndim == 2:  # grayscale
        pass
    elif converted.shape[2] == 3:  # RGB
        converted = converted[:, :, ::-1]
    elif converted.shape[2] == 4:  # RGBA
        converted = converted[:, :, [2, 1, 0, 3]]
    converted = Image.fromarray(converted)
    return converted


def pil2cv(img: Image.Image) -> np.ndarray:
    """Convert PIL->OpenCV.

    convert the format from PIL to OpenCV

    Args:
        img (PIL.Image.Imag): PIL image

    Returns:
        numpy.ndarray: OpenCV image

    """
    converted = np.array(img, dtype=np.uint8)
    if converted.ndim == 2:  # grayscale
        pass
    elif converted.shape[2] == 3:  # RGB
        converted = converted[:, :, ::-1]
    elif converted.shape[2] == 4:  # RGBA
        converted = converted[:, :, [2, 1, 0, 3]]
    return converted
