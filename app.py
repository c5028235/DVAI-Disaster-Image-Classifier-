# ==========================================
# Imports
# ==========================================

from ui.sidebar import render_sidebar
from ui.segmentation_tab import render_segmentation_tab
from ui.explainability_tab import render_explainability_tab
from ui.report_tab import render_report_tab
from ui.analytics_tab import render_analytics_tab
from ui.dashboard import (
    render_header,
    render_mission_brief,
    render_kpis
)

import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import time
from modules.model_loader import load_model
from modules.utils import load_image
from modules.inference import predict
from modules.confidence import class_statistics
from modules.export_images import (
    save_original,
    save_numpy
)

from modules.visualization import (
    create_segmentation_image,
    create_overlay,
    get_detected_classes,
    draw_mask_outline,
    create_class_mask
)
from modules.gradcam import (
    register_hooks,
    compute_gradcam,
    overlay_gradcam
)

from modules.report import (
    calculate_class_percentages,
    generate_summary,
    operational_assessment,
    recommendations
)
from modules.severity import calculate_severity
from modules.constants import CLASS_NAMES
from modules.pdf_report import create_pdf_report

# ==========================================
# Streamlit Configuration
# ==========================================

st.set_page_config(
    page_title="DisasterVision AI",
    page_icon="🚁",
    layout="wide"
)
render_header()

# ==========================================
# Load Model
# ==========================================

MODEL_PATH = "checkpoints/best_checkpoint.pth"


@st.cache_resource
def initialise_model():

    return load_model(MODEL_PATH)


model, device = initialise_model()

register_hooks(model)

# ==========================================
# Sidebar
# ==========================================

st.sidebar.title("🚁 DisasterVision AI")

uploaded_file = render_sidebar(device)

st.sidebar.success(f"Running on: {device}")

# ==========================================
# Main Page
# ==========================================

st.title("🚁 DisasterVision AI")

st.subheader(
    "Explainable Disaster Situation Awareness System"
)

if uploaded_file is None:

    st.info("Upload an image from the sidebar to begin.")

    st.stop()

# ==========================================
# Load Image
# ==========================================

image = load_image(uploaded_file)

# ==========================================
# Progress Indicator
# ==========================================

progress_text = st.empty()

progress_bar = st.progress(0)

progress_text.text("🚁 Uploading image...")
progress_bar.progress(15)

time.sleep(0.2)

prediction, probabilities, input_tensor = predict(
    model,
    device,
    image
)

progress_text.text("🧠 Running AI inference...")
progress_bar.progress(40)

time.sleep(0.2)

segmentation = create_segmentation_image(
    prediction
)

overlay = create_overlay(
    image,
    prediction
)

detected = get_detected_classes(
    prediction
)

percentages = calculate_class_percentages(
    prediction
)

severity = calculate_severity(percentages)

render_mission_brief(
    severity,
    percentages
)

render_kpis(
    severity,
    percentages
)

progress_text.text("🎨 Creating visualisations...")
progress_bar.progress(65)

time.sleep(0.2)

progress_bar.progress(100)

progress_text.success("✅ Analysis Complete")

time.sleep(0.5)

progress_bar.empty()

# ==========================================
# Tabs
# ==========================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🗺 Segmentation",
        "🔍 Explainability",
        "📊 Analytics",
        "📋 Report"
    ]
)

selected_class = int(np.unique(prediction)[1])  # first non-background class

heatmap = compute_gradcam(
    model,
    input_tensor,
    prediction,
    selected_class
)

gradcam_overlay = overlay_gradcam(
    image,
    heatmap
)
# ==========================================
# TAB 1
# ==========================================

with tab1:

    render_segmentation_tab(
        image,
        segmentation,
        overlay
    )

# ==========================================
# TAB 2
# ==========================================

with tab2:

    render_explainability_tab(
        model=model,
        image=image,
        prediction=prediction,
        probabilities=probabilities,
        input_tensor=input_tensor
    )
# ==========================================
# TAB 3
# ==========================================

with tab3:

    render_analytics_tab(
        severity,
        percentages,
        probabilities
    )


# ==========================================
# TAB 4
# ==========================================

with tab4:

    render_report_tab(
        image=image,
        segmentation=segmentation,
        gradcam_overlay=gradcam_overlay,
        severity=severity,
        percentages=percentages
    )
