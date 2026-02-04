"""
Views for the reports app.
"""

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CommunityIssue
from .serializers import CommunityIssueSerializer


def index(request):
    """Placeholder root view."""
    return HttpResponse(
        "Public Watch — Community Issue Reports API. Reports app is ready."
    )


def upload_page(request):
    """Render the frontend upload page."""
    return render(request, "reports/upload.html")


class IssueUploadView(APIView):
    """POST /api/issues/ — upload image and create a CommunityIssue."""

    def post(self, request):
        serializer = CommunityIssueSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        instance = serializer.save()
        response_serializer = CommunityIssueSerializer(
            instance, context={"request": request}
        )
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class IssueLocationView(APIView):
    """PATCH /api/issues/{id}/location/ — update issue latitude/longitude."""

    def patch(self, request, pk):
        try:
            issue = CommunityIssue.objects.get(pk=pk)
        except CommunityIssue.DoesNotExist:
            return Response(
                {"detail": "Not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        lat = request.data.get("latitude")
        lon = request.data.get("longitude")
        if lat is None or lon is None:
            return Response(
                {"detail": "latitude and longitude are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            lat = float(lat)
            lon = float(lon)
        except (TypeError, ValueError):
            return Response(
                {"detail": "latitude and longitude must be numbers."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            return Response(
                {"detail": "Invalid latitude or longitude range."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        issue.latitude = lat
        issue.longitude = lon
        issue.save(update_fields=["latitude", "longitude"])
        return Response(
            {"latitude": issue.latitude, "longitude": issue.longitude},
            status=status.HTTP_200_OK,
        )