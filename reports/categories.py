"""
Centralized category framework for community issue classification.

Single source of truth for main categories; use in AI prompts and mock.
"""

MAIN_CATEGORIES = [
    {
        "key": "roads_transport",
        "label": "Roads & Transport",
        "description": "Roads, pavements, traffic and transport.",
    },
    {
        "key": "water_sanitation",
        "label": "Water & Sanitation",
        "description": "Water supply, drainage, sewage, and sanitation.",
    },
    {
        "key": "waste_environment",
        "label": "Waste & Environment",
        "description": "Waste disposal, litter, pollution, environment.",
    },
    {
        "key": "public_facilities",
        "label": "Public Facilities",
        "description": "Parks, public buildings, and shared facilities.",
    },
    {
        "key": "safety_hazards",
        "label": "Safety & Hazards",
        "description": "Safety risks, hazards, and dangerous conditions.",
    },
    {
        "key": "housing_neighborhood",
        "label": "Housing & Neighborhood",
        "description": "Housing conditions and neighborhood issues.",
    },
    {
        "key": "accessibility_inclusion",
        "label": "Accessibility & Inclusion",
        "description": "Accessibility, inclusion, and equal access.",
    },
    {
        "key": "other",
        "label": "Other",
        "description": "Issues that do not fit the above; AI or human review.",
    },
]


def get_main_category_labels():
    """Return list of human-readable category labels for prompts/UI."""
    return [c["label"] for c in MAIN_CATEGORIES]


def get_category_by_key(key):
    """Return the category dict for a given key, or None."""
    for c in MAIN_CATEGORIES:
        if c["key"] == key:
            return c
    return None


def get_category_by_label(label):
    """Return the category dict for a given label, or None."""
    for c in MAIN_CATEGORIES:
        if c["label"] == label:
            return c
    return None
