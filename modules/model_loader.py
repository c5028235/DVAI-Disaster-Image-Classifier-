"""
Loads the trained DeepLabV3 model.
"""

import torch

from torchvision.models.segmentation import deeplabv3_resnet50
from torchvision.models.segmentation.deeplabv3 import DeepLabHead

from modules.constants import NUM_CLASSES


def load_model(checkpoint_path: str):

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    model = deeplabv3_resnet50(
        weights=None,
        weights_backbone=None,
        aux_loss=False
    )

    model.classifier = DeepLabHead(
        2048,
        NUM_CLASSES
    )

    checkpoint = torch.load(
        checkpoint_path,
        map_location=device
    )

    state_dict = checkpoint["model_state_dict"]

    state_dict = {
        k: v
        for k, v in state_dict.items()
        if not k.startswith("aux_classifier")
    }

    model.load_state_dict(
        state_dict,
        strict=False
    )

    model.to(device)

    model.eval()

    return model, device