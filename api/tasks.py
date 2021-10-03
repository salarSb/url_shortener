from celery import shared_task
from django.utils import timezone

from api.models import Link


@shared_task(name='delete_old_links')
def delete_old_links():
    links = Link.objects.all()
    for link in links:
        if link.expiration_date < timezone.now():
            link.delete()
    return f'completed deleting links at {timezone.now()}'
