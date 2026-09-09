"""
Situation Report Tab
"""

import streamlit as st

from modules.report import (
    generate_summary,
    operational_assessment,
    recommendations
)
from modules.pdf_report import create_pdf_report
from modules.export_images import (
    save_original,
    save_numpy
)


def render_report_tab(
    image,
    segmentation,
    gradcam_overlay,
    severity,
    percentages
):
    """
    Render the Situation Report tab.
    """

    summary = generate_summary(percentages)

    assessment = operational_assessment(percentages)

    actions = recommendations(percentages)

    st.header("📋 Disaster Situation Report")

    # =====================================
    # Disaster Severity
    # =====================================

    st.subheader("🚨 Disaster Severity Index")

    c1, c2 = st.columns([1, 2])

    with c1:

        st.metric(
            "Severity Score",
            f"{severity['score']} / 100"
        )

    with c2:

        colour = {
            "LOW": "green",
            "MODERATE": "orange",
            "HIGH": "darkorange",
            "CRITICAL": "red"
        }

        st.markdown(
            f"""
    <div style="
    padding:15px;
    border-radius:10px;
    background-color:{colour[severity['level']]};
    color:white;
    text-align:center;
    font-size:22px;
    font-weight:bold;
    ">
    {severity['level']}
    </div>
    """,
            unsafe_allow_html=True
        )

    st.divider()

    # =====================================
    # Executive Summary
    # =====================================

    st.subheader("Executive Summary")

    for item in summary:

        st.write(f"• {item}")

    st.divider()

    # =====================================
    # Class Statistics
    # =====================================

    st.subheader("Detected Classes")

    for cls, pct in percentages.items():

        if pct > 0:

            st.write(f"**{cls}** — {pct:.2f}%")

    st.divider()

    # =====================================
    # Operational Assessment
    # =====================================

    st.subheader("Operational Assessment")

    for item in assessment:

        st.write(f"• {item}")

    st.divider()

    # =====================================
    # Recommended Actions
    # =====================================

    st.subheader("Recommended Actions")

    for item in actions:

        st.write(f"• {item}")

    st.divider()

    # =====================================
    # PDF
    # =====================================

    original_path = save_original(image)

    segmentation_path = save_numpy(
        segmentation,
        "segmentation.png"
    )

    gradcam_path = save_numpy(
        gradcam_overlay,
        "gradcam.png"
    )

    create_pdf_report(
        "reports/Disaster_Report.pdf",
        severity,
        summary,
        percentages,
        assessment,
        actions,
        original_path,
        segmentation_path,
        gradcam_path
    )

    with open("reports/Disaster_Report.pdf", "rb") as pdf:

        st.download_button(
            "📄 Download Assessment Report",
            pdf,
            file_name="DisasterVision_Report.pdf",
            mime="application/pdf"
        )
