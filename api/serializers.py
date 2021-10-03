import string
from random import choices

from django.conf import settings
from django.utils import timezone
from rest_framework import serializers

from api.models import Link


def shortener():
    random_string = string.ascii_uppercase + string.ascii_lowercase + string.digits
    url_id = ''.join(choices(random_string, k=7))
    new_link = settings.HOST_URL + '/' + url_id
    return new_link


def five_minutes_hence():
    return timezone.now() + timezone.timedelta(minutes=5)


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'


class LinkCreateSerializer(serializers.ModelSerializer):
    expiration_date = serializers.DateTimeField(default=five_minutes_hence)
    shortened_link = serializers.URLField(default=shortener())

    class Meta:
        model = Link
        fields = ('original_link', 'shortened_link', 'expiration_date')

    def validate(self, data):
        if not data.get('shortened_link').startswith(settings.HOST_URL):
            shortened_url_error = 'shortened url must be starts with site domain'
            raise serializers.ValidationError(shortened_url_error)
        if data.get('expiration_date') < timezone.now():
            expiration_date_error = 'expiration date must be greater than created date'
            raise serializers.ValidationError(expiration_date_error)
        return data
