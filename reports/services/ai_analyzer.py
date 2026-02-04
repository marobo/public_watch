"""
Real AI image analysis integration layer.

This module is the single entry point for image-to-classification.
Replace the mock delegation with your AI provider (vision API, etc.)
when ready. Do not hardcode API keys; use environment or settings.
"""

from .ai_mock import analyze_image as _mock_analyze_image


def analyze_image(image_path):
    """
    Analyze an image and return structured community-issue classification.

    Args:
        image_path: Path to the image file (str or pathlib.Path).

    Returns:
        dict with keys: main_category, sub_category, severity, risks, description.
    """
    # TODO: Load AI provider config from env/settings (no keys in code).
    # TODO: Define prompts in a dedicated module, e.g. services/prompts.py.
    # TODO: Call real vision API here:
    #   - Send image (path or bytes) and prompt to provider
    #   - Parse provider response into the structure below
    #   - Handle rate limits, timeouts, errors; return fallback or raise
    # For now, delegate to mock so behavior matches Task 6.
    return _mock_analyze_image(image_path)
