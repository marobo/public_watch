"""
URL configuration for the reports app.
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("report/", views.upload_page),
    path("api/issues/", views.IssueUploadView.as_view()),
    path("api/issues/<int:pk>/location/", views.IssueLocationView.as_view()),
    path("api/issues/<int:pk>/status/", views.IssueStatusView.as_view()),
]
