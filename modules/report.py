"""
Situation Awareness Report Generator
"""

# ==========================================
# Imports
# ==========================================

import numpy as np

from modules.constants import CLASS_NAMES


# ==========================================
# Calculate Class Coverage
# ==========================================

def calculate_class_percentages(prediction):

    total_pixels = prediction.size

    percentages = {}

    for class_id, class_name in CLASS_NAMES.items():

        pixels = np.sum(prediction == class_id)

        percentages[class_name] = (pixels / total_pixels) * 100

    return percentages


# ==========================================
# Executive Summary
# ==========================================

def generate_summary(percentages):

    summary = []

    if percentages["Building_Total_Destruction"] > 1:
        summary.append(
            "Extensive structural destruction has been detected."
        )

    elif percentages["Building_Major_Damage"] > 1:
        summary.append(
            "Significant building damage has been detected."
        )

    else:
        summary.append(
            "No widespread structural collapse detected."
        )

    if percentages["Road-Blocked"] > 0.5:
        summary.append(
            "Road access is partially obstructed."
        )

    if percentages["Water"] > 5:
        summary.append(
            "Water bodies occupy a significant portion of the scene."
        )

    if percentages["Tree"] > 10:
        summary.append(
            "Vegetation remains largely intact."
        )

    return summary


# ==========================================
# Operational Assessment
# ==========================================

def operational_assessment(percentages):

    assessment = []

    if percentages["Building_Total_Destruction"] > 1:

        assessment.append(
            "Search and rescue operations should be prioritised."
        )

    if percentages["Road-Blocked"] > 0.5:

        assessment.append(
            "Emergency vehicle access may be restricted."
        )

    if percentages["Vehicle"] > 2:

        assessment.append(
            "Vehicles detected within the affected area."
        )

    if len(assessment) == 0:

        assessment.append(
            "No major operational concerns identified."
        )

    return assessment


# ==========================================
# Recommended Actions
# ==========================================

def recommendations(percentages):

    actions = []

    if percentages["Building_Total_Destruction"] > 1:

        actions.append(
            "Deploy Urban Search and Rescue teams."
        )

    if percentages["Road-Blocked"] > 0.5:

        actions.append(
            "Clear blocked roads to restore emergency access."
        )

    if percentages["Building_Major_Damage"] > 1:

        actions.append(
            "Inspect unstable structures before entry."
        )

    if percentages["Water"] > 5:

        actions.append(
            "Assess potential flood impacts."
        )

    if len(actions) == 0:

        actions.append(
            "Continue monitoring the area."
        )

    return actions