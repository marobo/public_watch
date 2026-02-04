"""
Views for the reports app.
"""

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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