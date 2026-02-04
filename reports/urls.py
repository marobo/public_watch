"""
URL configuration for the reports app.
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("report/", views.upload_page),
    path("api/issues/", views.IssueUploadView.as_view()),
]
