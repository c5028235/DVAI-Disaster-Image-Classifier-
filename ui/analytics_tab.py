"""
Analytics Dashboard
"""

import streamlit as st

from modules.charts import (
    plot_class_distribution,
    plot_pie_chart,
    plot_confidence_histogram
)


def render_analytics_tab(
    severity,
    percentages,
    probabilities
):

    st.header("📊 Analytics Dashboard")

    st.subheader("Model Summary")

    c1, c2, c3 = st.columns(3)

    detected = sum(
        pct > 0
        for pct in percentages.values()
    )

    c1.metric(
        "Detected Classes",
        detected
    )

    c2.metric(
        "Severity Score",
        severity["score"]
    )

    c3.metric(
        "Severity",
        severity["level"]
    )

    st.divider()

    st.subheader("Class Coverage")

    fig = plot_class_distribution(
        percentages
    )

    st.pyplot(fig)

    st.divider()

    st.subheader("Scene Composition")

    fig = plot_pie_chart(
        percentages
    )

    st.pyplot(fig)

    st.divider()

    st.subheader("Confidence Distribution")

    fig = plot_confidence_histogram(
        probabilities
    )

    st.pyplot(fig)
