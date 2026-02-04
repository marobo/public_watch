"""
Create sample CommunityIssue records for demo and development.
"""

import io

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from reports.categories import MAIN_CATEGORIES
from reports.models import CommunityIssue


def make_placeholder_image():
    """Return bytes of a minimal valid PNG (1x1 pixel)."""
    try:
        from PIL import Image
    except ImportError:
        raise ImportError("Pillow required for seed_issues. pip install Pillow")
    buf = io.BytesIO()
    img = Image.new("RGB", (1, 1), color=(128, 128, 128))
    img.save(buf, format="PNG")
    return buf.getvalue()


SEED_DATA = [
    {
        "main_category": MAIN_CATEGORIES[0]["label"],
        "sub_category": "Pothole",
        "severity": "high",
        "status": "new",
        "latitude": 40.7128,
        "longitude": -74.0060,
    },
    {
        "main_category": MAIN_CATEGORIES[1]["label"],
        "sub_category": "Leaking pipe",
        "severity": "medium",
        "status": "review",
        "latitude": 34.0522,
        "longitude": -118.2437,
    },
    {
        "main_category": MAIN_CATEGORIES[2]["label"],
        "sub_category": "Dumped waste",
        "severity": "high",
        "status": "new",
        "latitude": None,
        "longitude": None,
    },
    {
        "main_category": MAIN_CATEGORIES[3]["label"],
        "sub_category": "Broken bench",
        "severity": "low",
        "status": "fixed",
        "latitude": 51.5074,
        "longitude": -0.1278,
    },
    {
        "main_category": MAIN_CATEGORIES[4]["label"],
        "sub_category": "Exposed wiring",
        "severity": "high",
        "status": "review",
        "latitude": None,
        "longitude": None,
    },
    {
        "main_category": MAIN_CATEGORIES[5]["label"],
        "sub_category": "Structural crack",
        "severity": "medium",
        "status": "new",
        "latitude": 48.8566,
        "longitude": 2.3522,
    },
    {
        "main_category": MAIN_CATEGORIES[6]["label"],
        "sub_category": "Missing ramp",
        "severity": "medium",
        "status": "new",
        "latitude": None,
        "longitude": None,
    },
    {
        "main_category": MAIN_CATEGORIES[7]["label"],
        "sub_category": "Uncategorized",
        "severity": "low",
        "status": "new",
        "latitude": -33.8688,
        "longitude": 151.2093,
    },
    {
        "main_category": MAIN_CATEGORIES[0]["label"],
        "sub_category": "Cracked pavement",
        "severity": "low",
        "status": "fixed",
        "latitude": 35.6762,
        "longitude": 139.6503,
    },
    {
        "main_category": MAIN_CATEGORIES[2]["label"],
        "sub_category": "Overflowing bin",
        "severity": "medium",
        "status": "review",
        "latitude": None,
        "longitude": None,
    },
]


class Command(BaseCommand):
    help = "Create sample CommunityIssue records (at least 10) for demo/dev."

    def handle(self, *args, **options):
        png_bytes = make_placeholder_image()
        created = 0
        for i, data in enumerate(SEED_DATA):
            name = f"issues/seed_{i + 1}.png"
            CommunityIssue.objects.create(
                image=ContentFile(png_bytes, name=name),
                main_category=data["main_category"],
                sub_category=data["sub_category"],
                severity=data["severity"],
                risks=["safety"] if data["severity"] == "high" else [],
                description=f"Seed issue: {data['sub_category']}.",
                latitude=data["latitude"],
                longitude=data["longitude"],
                status=data["status"],
            )
            created += 1
        msg = f"Created {created} CommunityIssue(s)."
        self.stdout.write(self.style.SUCCESS(msg))
