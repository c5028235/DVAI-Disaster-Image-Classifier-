"""
Inference functions for DisasterVision AI.
"""

# ==========================================
# Imports
# ==========================================

import numpy as np
import torch
import albumentations as A

from PIL import Image
from albumentations.pytorch import ToTensorV2

# ==========================================
# Image Transform
# ==========================================

transform = A.Compose([
    A.Resize(512, 512),
    A.Normalize(),
    ToTensorV2()
])

# ==========================================
# Preprocessing
# ==========================================

def preprocess_image(image: Image.Image):
    """
    Convert a PIL image into a tensor suitable for DeepLabV3.
    """

    image_np = np.array(image)

    transformed = transform(image=image_np)

    input_tensor = transformed["image"].unsqueeze(0)

    return input_tensor


# ==========================================
# Prediction
# ==========================================

def predict(model, device, image):

    input_tensor = preprocess_image(image)

    input_tensor = input_tensor.to(device)

    with torch.no_grad():

        output = model(input_tensor)["out"]

        probabilities = torch.softmax(
            output,
            dim=1
        )

    prediction = torch.argmax(
        probabilities,
        dim=1
    )

    prediction = prediction.squeeze().cpu().numpy()

    probabilities = probabilities.squeeze().cpu().numpy()

    return prediction, probabilities, input_tensor