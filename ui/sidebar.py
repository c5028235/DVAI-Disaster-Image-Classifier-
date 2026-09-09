import streamlit as st


def render_sidebar(device):

    with st.sidebar:

        # st.image(
        #     "assets/logo.png",
        #     use_container_width=True
        # )

        st.title("DisasterVision AI")

        st.markdown("---")

        uploaded = st.file_uploader(
            "Upload UAV Image",
            type=[
                "jpg",
                "jpeg",
                "png"
            ]
        )

        st.markdown("---")

        st.subheader("System Status")

        st.success("✅ Model Loaded")

        st.success("✅ Explainability Ready")

        st.success("✅ Report Generator Ready")

        if device.type == "cuda":

            st.success("🟢 GPU Available")

        else:

            st.warning("🟡 CPU Mode")

        st.markdown("---")

        st.caption("Version 2.0")

    return uploaded
