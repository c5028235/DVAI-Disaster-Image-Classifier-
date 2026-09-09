"""
Export images for PDF reports.
"""

import os
import cv2
import numpy as np
from PIL import Image


EXPORT_FOLDER = "temp"


def ensure_folder():
    os.makedirs(EXPORT_FOLDER, exist_ok=True)


def save_original(image):
    """
    Save uploaded PIL image.
    """
    ensure_folder()

    path = os.path.join(EXPORT_FOLDER, "original.png")

    image.save(path)

    return path


def save_numpy(image, filename):
    """
    Save either a PIL Image or a NumPy array.
    """

    ensure_folder()

    path = os.path.join(EXPORT_FOLDER, filename)

    # Convert PIL Image to NumPy
    if isinstance(image, Image.Image):
        image = np.array(image)

    # Convert to uint8 if necessary
    if image.dtype != np.uint8:
        image = image.astype(np.uint8)

    # Convert RGB to BGR for OpenCV
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    cv2.imwrite(path, image)

    return path
