import logging
from django.db import models

logger = logging.getLogger(__name__)


class PostmarkWebhook(models.Model):
    received_at = models.DateTimeField(auto_now_add=True)
    body = models.JSONField()
    headers = models.JSONField()
    note = models.TextField(blank=True)

    class Status(models.TextChoices):
        NEW = "new"
        PROCESSED = "processed"
        ERROR = "error"

    status = models.CharField(
        max_length=127, choices=Status.choices, default=Status.NEW
    )
