"""
Disaster Severity Index (DSI)
"""

def calculate_severity(percentages):
    """
    Calculates a severity score (0–100)
    based on class coverage.
    """

    score = 0

    # Cap each contribution to avoid runaway scores
    score += min(percentages["Building_Total_Destruction"] / 5, 1) * 40
    score += min(percentages["Building_Major_Damage"] / 5, 1) * 20
    score += min(percentages["Building_Minor_Damage"] / 5, 1) * 10
    score += min(percentages["Road-Blocked"] / 5, 1) * 20
    score += min(percentages["Water"] / 20, 1) * 5
    score += min(percentages["Vehicle"] / 10, 1) * 5

    score = round(score, 1)

    if score < 25:
        level = "LOW"
        colour = "green"

    elif score < 50:
        level = "MODERATE"
        colour = "orange"

    elif score < 75:
        level = "HIGH"
        colour = "darkorange"

    else:
        level = "CRITICAL"
        colour = "red"

    return {
        "score": score,
        "level": level,
        "colour": colour
    }