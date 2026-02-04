"""
Mock AI image analysis service for development and testing.

Returns a fixed classification; no external APIs are called.
Uses reports.categories for consistent main category labels.
"""

from reports.categories import MAIN_CATEGORIES


def analyze_image(image_path):
    """
    Simulate AI analysis of an image for community issue classification.

    Args:
        image_path: Path to the image file (unused in mock; for API compat).

    Returns:
        dict: main_category, sub_category, severity, risks, description.
    """
    roads = next(c for c in MAIN_CATEGORIES if c["key"] == "roads_transport")
    return {
        "main_category": roads["label"],
        "sub_category": "Pothole",
        "severity": "high",
        "risks": ["safety"],
        "description": "Visible pothole causing unsafe driving conditions.",
    }
