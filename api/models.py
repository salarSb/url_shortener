from django.db import models


class Link(models.Model):
    original_link = models.URLField()
    shortened_link = models.URLField(unique=True)
    times_followed = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()
