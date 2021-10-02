from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.generics import ListAPIView, CreateAPIView

from api.models import Link
from api.serializers import LinkSerializer, LinkCreateSerializer


class ShortenerListAPIView(ListAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class ShortenerCreateAPIView(CreateAPIView):
    serializer_class = LinkCreateSerializer


def redirect_url_view(request, shortened_part):
    shortener_link = settings.HOST_URL + '/' + shortened_part
    try:
        shortener = Link.objects.get(shortened_link=shortener_link)
        shortener.times_followed += 1
        shortener.save()
        return redirect(shortener.original_link)
    except Link.DoesNotExist:
        return JsonResponse({'success': False})
