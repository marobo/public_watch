"""
Real AI image analysis integration layer.

This module is the single entry point for image-to-classification.
Replace the mock delegation with your AI provider (vision API, etc.)
when ready. Do not hardcode API keys; use environment or settings.
Logs failures to the reports.ai logger for production debugging.
"""

import logging

from .ai_mock import analyze_image as _mock_analyze_image

logger = logging.getLogger("reports.ai")


def analyze_image(image_path):
    """
    Analyze an image and return structured community-issue classification.

    Args:
        image_path: Path to the image file (str or pathlib.Path).

    Returns:
        dict with keys: main_category, sub_category, severity, risks, description.

    Raises:
        Exception: Propagates any exception from the underlying AI/mock implementation.
        Failures are logged to reports.ai before re-raising.
    """
    # TODO: When building the prompt, use get_main_category_labels() from
    # reports.categories so the model chooses from the canonical list.
    # TODO: Load AI provider config from env/settings (no keys in code).
    # TODO: Define prompts in a dedicated module, e.g. services/prompts.py.
    # TODO: Call real vision API here; handle rate limits, timeouts, errors.
    try:
        return _mock_analyze_image(image_path)
    except Exception as exc:
        logger.warning("AI analysis failed for image %s: %s", image_path, exc)
        raise
