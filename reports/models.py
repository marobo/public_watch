from django.db import models


class CommunityIssue(models.Model):
    """A single community-reported issue (e.g. pothole, waste, hazard)."""

    SEVERITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    STATUS_CHOICES = [
        ("new", "New"),
        ("review", "Review"),
        ("fixed", "Fixed"),
    ]

    image = models.ImageField(upload_to="issues/")
    main_category = models.CharField(max_length=50)
    sub_category = models.CharField(max_length=100)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    risks = models.JSONField(default=list)  # list of strings
    description = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="new"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Community issue"
        verbose_name_plural = "Community issues"

    def __str__(self):
        return f"{self.main_category} — {self.get_severity_display()}"
