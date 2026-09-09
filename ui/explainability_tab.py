"""
Explainability Tab
"""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from modules.constants import CLASS_NAMES
from modules.confidence import class_statistics
from modules.gradcam import (
    compute_gradcam,
    overlay_gradcam
)
from modules.visualization import (
    draw_mask_outline,
    create_class_mask
)


def render_explainability_tab(
    model,
    image,
    prediction,
    probabilities,
    input_tensor
):
    """
    Render the Explainability tab.
    """

    st.header("🔍 Explainability")

    available_classes = sorted(np.unique(prediction))

    # Remove background
    available_classes = [
        c for c in available_classes
        if c != 0
    ]

    if len(available_classes) == 0:

        st.warning("Only background detected.")

        return

    selected = st.selectbox(
        "Choose a class",
        available_classes,
        format_func=lambda x: CLASS_NAMES[x]
    )

    stats = class_statistics(
        prediction,
        probabilities,
        selected
    )

    with st.spinner("Generating Grad-CAM..."):

        heatmap = compute_gradcam(
            model,
            input_tensor,
            prediction,
            selected
        )

    if heatmap is None:

        st.warning("Unable to generate Grad-CAM.")

        return

    gradcam_overlay = overlay_gradcam(
        image,
        heatmap
    )

    outlined = draw_mask_outline(
        image,
        prediction,
        selected
    )

    class_mask = create_class_mask(
        prediction,
        selected
    )

    # =====================================
    # Images
    # =====================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.image(
            outlined,
            caption="Detected Region",
            use_container_width=True
        )

    with col2:

        st.image(
            class_mask,
            caption="Predicted Mask",
            use_container_width=True
        )

    with col3:

        st.image(
            gradcam_overlay,
            caption="Grad-CAM",
            use_container_width=True
        )

    st.divider()

    # =====================================
    # Confidence Metrics
    # =====================================

    st.subheader("Prediction Confidence")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Coverage",
        f"{stats['coverage']:.2f}%"
    )

    c2.metric(
        "Average",
        f"{stats['mean']:.2f}%"
    )

    c3.metric(
        "Maximum",
        f"{stats['max']:.2f}%"
    )

    c4.metric(
        "Minimum",
        f"{stats['min']:.2f}%"
    )

    st.divider()

    # =====================================
    # Confidence Heatmap
    # =====================================

    st.subheader("Confidence Heatmap")

    fig, ax = plt.subplots(figsize=(6, 6))

    confidence_map = stats["heatmap"]

    im = ax.imshow(
        confidence_map,
        cmap="viridis",
        vmin=0,
        vmax=1
    )

    ax.set_title(
        f"{CLASS_NAMES[selected]} Confidence"
    )

    ax.axis("off")

    fig.colorbar(im, ax=ax)

    st.pyplot(fig)

    plt.close(fig)

    st.divider()

    # =====================================
    # AI Explanation
    # =====================================

    st.subheader("AI Explanation")

    st.success(
        f"""
The model classified these pixels as **{CLASS_NAMES[selected]}**.

**Coverage:** {stats['coverage']:.2f}% of the analysed image.

The left panel shows the detected object boundary.

The middle panel shows only the pixels belonging to the selected semantic class.

The Grad-CAM highlights the regions that contributed most strongly to the model's prediction.

The confidence heatmap visualises the model's confidence for this class across the entire image.
"""
    )