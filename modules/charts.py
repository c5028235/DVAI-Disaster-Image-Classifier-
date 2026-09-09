"""
Charts Module
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_class_distribution(percentages):

    labels = []
    values = []

    for cls, pct in percentages.items():

        if pct > 0:

            labels.append(cls.replace("_", "\n"))

            values.append(pct)

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(labels, values)

    ax.set_ylabel("Coverage (%)")

    ax.set_title("Class Coverage")

    plt.xticks(rotation=45)

    plt.tight_layout()

    return fig


def plot_pie_chart(percentages):
    """
    Professional Scene Composition Pie Chart
    """

    labels = []
    values = []

    for cls, pct in percentages.items():

        if pct > 0:
            labels.append(cls.replace("_", " "))
            values.append(pct)

    fig, ax = plt.subplots(figsize=(10, 7))

    wedges, texts, autotexts = ax.pie(
        values,
        labels=None,                 # Don't put class names on slices
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=0.7,
        textprops={"fontsize": 11},
        wedgeprops={
            "edgecolor": "white",
            "linewidth": 2
        }
    )

    # Make percentage text bold
    for autotext in autotexts:
        autotext.set_fontsize(11)
        autotext.set_weight("bold")
        autotext.set_color("black")

    # Add legend outside the chart
    legend_labels = [
        f"{label} ({value:.1f}%)"
        for label, value in zip(labels, values)
    ]

    ax.legend(
        wedges,
        legend_labels,
        title="Classes",
        loc="center left",
        bbox_to_anchor=(1.0, 0.5),
        fontsize=10,
        title_fontsize=11
    )

    ax.set_title(
        "Scene Composition",
        fontsize=16,
        fontweight="bold"
    )

    plt.tight_layout()

    return fig


def plot_confidence_histogram(probabilities):

    confidence = np.max(
        probabilities,
        axis=0
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.hist(
        confidence.flatten(),
        bins=25
    )

    ax.set_xlabel("Confidence")

    ax.set_ylabel("Pixels")

    ax.set_title("Prediction Confidence")

    return fig
