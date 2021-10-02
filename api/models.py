import string
from random import choices

from django.conf import settings
from django.db import models


def shortener():
    random_string = string.ascii_uppercase + string.ascii_lowercase + string.digits
    url_id = ''.join(choices(random_string, k=7))
    new_link = settings.HOST_URL + '/' + url_id
    return new_link


class Link(models.Model):
    original_link = models.URLField()
    shortened_link = models.URLField(null=True, blank=True, unique=True)
    times_followed = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.shortened_link:
            new_link = shortener()
            self.shortened_link = new_link
        return super(Link, self).save(*args, **kwargs)
