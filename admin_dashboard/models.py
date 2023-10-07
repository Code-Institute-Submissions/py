from django.db import models
from homepage.models import UserProfile


class OrderDeletionRecord(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    initiated_by = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True)
    # Add any other fields you might find useful
