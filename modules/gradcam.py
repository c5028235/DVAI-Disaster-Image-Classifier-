"""
Custom Grad-CAM for DeepLabV3 semantic segmentation.
"""

# =====================================================
# Imports
# =====================================================

import cv2
import numpy as np
import torch

# =====================================================
# Global hook variables
# =====================================================

features = None
gradients = None


# =====================================================
# Hook functions
# =====================================================

def forward_hook(module, input, output):
    global features
    features = output


def backward_hook(module, grad_input, grad_output):
    global gradients
    gradients = grad_output[0]


# =====================================================
# Register hooks
# =====================================================

def register_hooks(model):

    target_layer = model.backbone.layer4

    target_layer.register_forward_hook(
        forward_hook
    )

    target_layer.register_full_backward_hook(
        backward_hook
    )


# =====================================================
# Compute Grad-CAM
# =====================================================

def compute_gradcam(
    model,
    input_tensor,
    prediction,
    target_class
):

    global features
    global gradients

    model.zero_grad()

    output = model(input_tensor)["out"]

    mask = prediction == target_class

    if mask.sum() == 0:
        return None

    score = output[0, target_class][mask].mean()

    score.backward()

    weights = gradients.mean(
        dim=(2, 3),
        keepdim=True
    )

    cam = (weights * features).sum(dim=1)

    cam = torch.relu(cam)

    cam -= cam.min()

    cam /= (cam.max() + 1e-8)

    cam = cam.squeeze().detach().cpu().numpy()

    cam = cv2.resize(
        cam,
        (512, 512)
    )

    return cam


# =====================================================
# Overlay
# =====================================================

def overlay_gradcam(
    original_image,
    heatmap
):

    image = np.array(
        original_image.resize((512, 512))
    )

    heatmap = np.uint8(
        255 * heatmap
    )

    heatmap = cv2.applyColorMap(
        heatmap,
        cv2.COLORMAP_JET
    )

    heatmap = cv2.cvtColor(
        heatmap,
        cv2.COLOR_BGR2RGB
    )

    overlay = cv2.addWeighted(
        image,
        0.65,
        heatmap,
        0.35,
        0
    )

    return overlay