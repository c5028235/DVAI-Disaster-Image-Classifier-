"""
Utility functions.
"""

# ==========================
# Imports
# ==========================

from pathlib import Path

from PIL import Image


def load_image(uploaded_file):
    """
    Load an uploaded Streamlit image.

    Parameters
    ----------
    uploaded_file : UploadedFile

    Returns
    -------
    PIL.Image
    """

    image = Image.open(uploaded_file)

    image = image.convert("RGB")

    return image


def ensure_output_folder():

    Path("outputs").mkdir(
        exist_ok=True
    )