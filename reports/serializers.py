"""
Serializers for the reports app.
"""

import logging

from rest_framework import serializers

from .models import CommunityIssue
from .services.ai_analyzer import analyze_image
from .utils import extract_gps_from_image

logger = logging.getLogger("reports.upload")


class CommunityIssueSerializer(serializers.ModelSerializer):
    """Accepts image on create; returns id, image_url, status, created_at, optional lat/lon."""

    image_url = serializers.SerializerMethodField()

    class Meta:
        model = CommunityIssue
        fields = (
            "id",
            "image_url",
            "status",
            "created_at",
            "latitude",
            "longitude",
            "image",
        )
        extra_kwargs = {"image": {"write_only": True, "required": True}}

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None

    def create(self, validated_data):
        instance = CommunityIssue.objects.create(
            image=validated_data["image"],
            status="new",
            main_category="",
            sub_category="",
            severity="low",
            risks=[],
            description="",
        )
        lat, lon = extract_gps_from_image(instance.image.path)
        if lat is not None and lon is not None:
            instance.latitude = lat
            instance.longitude = lon

        try:
            analysis = analyze_image(instance.image.path)
        except Exception as exc:
            logger.warning("Image upload: AI analysis failed for issue %s: %s", instance.pk, exc)
            raise
        instance.main_category = analysis["main_category"]
        instance.sub_category = analysis["sub_category"]
        instance.severity = analysis["severity"]
        instance.risks = analysis["risks"]
        instance.description = analysis["description"]

        update_fields = [
            "main_category",
            "sub_category",
            "severity",
            "risks",
            "description",
        ]
        if lat is not None and lon is not None:
            update_fields.extend(["latitude", "longitude"])
        instance.save(update_fields=update_fields)
        return instance
