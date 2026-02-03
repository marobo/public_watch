"""
Serializers for the reports app.
"""

from rest_framework import serializers

from .models import CommunityIssue


class CommunityIssueSerializer(serializers.ModelSerializer):
    """Accepts image on create; returns id, image_url, status, created_at."""

    image_url = serializers.SerializerMethodField()

    class Meta:
        model = CommunityIssue
        fields = ("id", "image_url", "status", "created_at", "image")
        extra_kwargs = {"image": {"write_only": True, "required": True}}

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None

    def create(self, validated_data):
        return CommunityIssue.objects.create(
            image=validated_data["image"],
            status="new",
            main_category="",
            sub_category="",
            severity="low",
            risks=[],
            description="",
        )
