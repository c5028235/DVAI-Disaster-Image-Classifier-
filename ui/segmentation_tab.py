"""
Segmentation Tab
"""

import streamlit as st


def render_segmentation_tab(
    image,
    segmentation,
    overlay
):

    st.header("🗺 Semantic Segmentation")

    col1, col2 = st.columns(2)

    with col1:

        st.image(
            image,
            caption="Original Image",
            use_container_width=True
        )

    with col2:

        st.image(
            segmentation,
            caption="Predicted Segmentation",
            use_container_width=True
        )

    st.divider()

    st.image(
        overlay,
        caption="Segmentation Overlay",
        use_container_width=True
    )