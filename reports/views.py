"""
Views for the reports app.
Models and API endpoints will be added in later tasks.
"""

from django.http import HttpResponse


def index(request):
    """Placeholder root view."""
    return HttpResponse("Public Watch — Community Issue Reports API. Reports app is ready.")
