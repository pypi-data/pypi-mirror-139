from django.db import models
from model_utils import Choices


EVENT_STATUS_CHOICES = Choices("PENDING", "FAILED", "SUCCESS")


class EventDetails(models.Model):
    event_id = models.UUIDField(primary_key=True, unique=True)
    adapter = models.CharField(max_length=30, db_index=True)
    status = models.CharField(
        max_length=20,
        choices=EVENT_STATUS_CHOICES,
        default=EVENT_STATUS_CHOICES.PENDING,
        db_index=True,
    )
    data = models.JSONField(default=dict, null=True, blank=True)
    result = models.TextField(null=True, blank=True)
    error = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    @property
    def short_data(self):
        return self.data[:100]
