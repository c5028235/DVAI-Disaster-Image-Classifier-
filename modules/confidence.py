"""
Confidence analysis utilities.
"""

import numpy as np


def class_statistics(prediction, probabilities, target_class):

    mask = prediction == target_class

    if mask.sum() == 0:

        return None

    confidence = probabilities[target_class]

    values = confidence[mask]

    coverage = (
        mask.sum()
        / mask.size
    ) * 100

    return {

        "coverage": coverage,

        "mean": values.mean() * 100,

        "max": values.max() * 100,

        "min": values.min() * 100,

        "heatmap": confidence

    }