"""
Dashboard Components
"""

import streamlit as st


def render_header():

    st.title("🚁 DisasterVision AI")

    st.caption(
        "AI-Powered Post-Disaster Damage Assessment using Semantic Segmentation and Explainable AI"
    )

    st.divider()


def render_mission_brief(
    severity,
    percentages
):

    st.subheader("🛰 Mission Brief")

    if severity["level"] == "CRITICAL":

        colour = "🔴"

    elif severity["level"] == "HIGH":

        colour = "🟠"

    elif severity["level"] == "MODERATE":

        colour = "🟡"

    else:

        colour = "🟢"

    destroyed = percentages.get(
        "Building_Total_Destruction",
        0
    )

    blocked = percentages.get(
        "Road-Blocked",
        0
    )

    road_status = (
        "Restricted"
        if blocked > 0.5
        else "Accessible"
    )

    if destroyed > 1:

        response = (
            "Deploy Urban Search & Rescue teams."
        )

    else:

        response = (
            "Continue monitoring."
        )

    st.info(
        f"""
Priority Level: **{colour} {severity['level']}**

**Road Status:** {road_status}

**Destroyed Buildings:** {destroyed:.2f}%

**Immediate Recommendation:**

{response}
"""
    )

    st.divider()


def render_kpis(
    severity,
    percentages
):

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Severity",
        severity["score"]
    )

    c2.metric(
        "Destroyed",
        f"{percentages['Building_Total_Destruction']:.2f}%"
    )

    c3.metric(
        "Road Blocked",
        f"{percentages['Road-Blocked']:.2f}%"
    )

    c4.metric(
        "Trees",
        f"{percentages['Tree']:.2f}%"
    )

    st.divider()
