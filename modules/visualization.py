"""
Visualization functions for DisasterVision AI.
"""

# ==========================================
# Imports
# ==========================================


import cv2
import numpy as np
from PIL import Image

from matplotlib.colors import ListedColormap

from modules.constants import CLASS_NAMES

# ==========================================
# Color Map
# ==========================================

CLASS_COLORS = np.array([
    [0, 0, 0],          # Background
    [0, 0, 255],        # Water
    [0, 255, 0],        # Building_No_Damage
    [144, 238, 144],    # Building_Minor_Damage
    [255, 165, 0],      # Building_Major_Damage
    [255, 0, 0],        # Building_Total_Destruction
    [128, 0, 128],      # Vehicle
    [139, 69, 19],      # Road-Clear
    [255, 20, 147],     # Road-Blocked
    [0, 255, 255],      # Tree
    [255, 255, 0]       # Pool
], dtype=np.uint8)

# ==========================================
# Segmentation Image
# ==========================================

def create_segmentation_image(prediction):

    rgb = CLASS_COLORS[prediction]

    return Image.fromarray(rgb)


# ==========================================
# Overlay
# ==========================================

def create_overlay(original_image, prediction, alpha=0.4):

    original = np.array(original_image.resize((512, 512)))

    segmentation = CLASS_COLORS[prediction]

    overlay = (
        alpha * segmentation +
        (1 - alpha) * original
    ).astype(np.uint8)

    return Image.fromarray(overlay)


# ==========================================
# Legend
# ==========================================

def get_detected_classes(prediction):

    detected = np.unique(prediction)

    return [
        (CLASS_NAMES[int(cls)], CLASS_COLORS[int(cls)])
        for cls in detected
    ]

def create_class_mask(prediction, target_class):
    """
    Create a binary mask for the selected class.
    """

    mask = (prediction == target_class).astype(np.uint8)

    return mask * 255

def draw_mask_outline(original_image, prediction, target_class):
    """
    Draw the outline of the selected class on the image.
    """

    image = np.array(
        original_image.resize((512, 512))
    ).copy()

    mask = create_class_mask(
        prediction,
        target_class
    )

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    cv2.drawContours(
        image,
        contours,
        -1,
        (255, 255, 0),
        2
    )

    return image