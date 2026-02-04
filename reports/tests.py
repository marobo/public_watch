"""
Basic tests for the reports app.
"""

import io
import os
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from .models import CommunityIssue
from .utils import extract_gps_from_image


def make_minimal_png():
    """Return bytes of a minimal valid PNG (1x1 pixel, no EXIF)."""
    try:
        from PIL import Image
    except ImportError:
        raise ImportError("Pillow required for tests")
    buf = io.BytesIO()
    Image.new("RGB", (1, 1), color=(128, 128, 128)).save(buf, format="PNG")
    return buf.getvalue()


class ImageUploadAPITest(TestCase):
    """Image upload API returns 201 and creates CommunityIssue."""

    def setUp(self):
        self.client = APIClient()

    def test_upload_returns_201_and_creates_issue(self):
        png = make_minimal_png()
        response = self.client.post(
            "/api/issues/",
            {"image": SimpleUploadedFile("test.png", png, "image/png")},
            format="multipart",
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn("id", data)
        self.assertIn("status", data)
        self.assertEqual(data["status"], "new")
        self.assertEqual(CommunityIssue.objects.count(), 1)
        issue = CommunityIssue.objects.get(pk=data["id"])
        self.assertEqual(issue.status, "new")


class GPSExtractionTest(TestCase):
    """GPS extraction utility does not crash without EXIF."""

    def test_no_crash_without_exif(self):
        png = make_minimal_png()
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(png)
            path = f.name
        try:
            lat, lon = extract_gps_from_image(path)
            self.assertIsNone(lat)
            self.assertIsNone(lon)
        finally:
            os.unlink(path)

    def test_nonexistent_path_returns_none(self):
        lat, lon = extract_gps_from_image("/nonexistent/path/image.jpg")
        self.assertIsNone(lat)
        self.assertIsNone(lon)


class MockAITest(TestCase):
    """Mock AI fills category and severity fields on upload."""

    def setUp(self):
        self.client = APIClient()

    def test_upload_fills_category_and_severity(self):
        png = make_minimal_png()
        response = self.client.post(
            "/api/issues/",
            {"image": SimpleUploadedFile("test.png", png, "image/png")},
            format="multipart",
        )
        self.assertEqual(response.status_code, 201)
        issue_id = response.json()["id"]
        issue = CommunityIssue.objects.get(pk=issue_id)
        self.assertEqual(issue.main_category, "Roads & Transport")
        self.assertEqual(issue.sub_category, "Pothole")
        self.assertEqual(issue.severity, "high")
        self.assertEqual(issue.description, "Visible pothole causing unsafe driving conditions.")


class StatusWorkflowTest(TestCase):
    """Status workflow allows valid transitions and rejects invalid ones."""

    def setUp(self):
        self.client = APIClient()
        png = make_minimal_png()
        resp = self.client.post(
            "/api/issues/",
            {"image": SimpleUploadedFile("test.png", png, "image/png")},
            format="multipart",
        )
        self.assertEqual(resp.status_code, 201, resp.content)
        self.issue_id = resp.json()["id"]

    def test_valid_new_to_review(self):
        response = self.client.patch(
            f"/api/issues/{self.issue_id}/status/",
            {"status": "review"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "review")
        self.assertEqual(CommunityIssue.objects.get(pk=self.issue_id).status, "review")

    def test_valid_review_to_fixed(self):
        self.client.patch(
            f"/api/issues/{self.issue_id}/status/",
            {"status": "review"},
            format="json",
        )
        response = self.client.patch(
            f"/api/issues/{self.issue_id}/status/",
            {"status": "fixed"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "fixed")

    def test_invalid_new_to_fixed_rejected(self):
        response = self.client.patch(
            f"/api/issues/{self.issue_id}/status/",
            {"status": "fixed"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.json())
        self.assertEqual(CommunityIssue.objects.get(pk=self.issue_id).status, "new")
