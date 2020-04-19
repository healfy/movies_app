import requests
from rest_framework import serializers

from .models import Movie
from .tasks import convert_video
from .utils import nested_commit_on_success
from django.db import transaction
from django.conf import settings


class MovieSerializer(serializers.ModelSerializer):
    db_file = serializers.FileField(required=False)

    class Meta:
        model = Movie
        fields = ('db_file',)

    @nested_commit_on_success
    def create(self, validated_data):
        instance = super().create(validated_data)
        transaction.on_commit(
            lambda: convert_video.apply_async(
                args=(instance._meta.app_label,
                      instance._meta.model_name,
                      instance.pk)
            )
        )
        return instance


class URLSerializer(serializers.Serializer):
    url = serializers.URLField()

    def validate(self, attrs):
        attrs = super(URLSerializer, self).validate(attrs)
        if not self.is_downloadable(attrs['url']):
            raise serializers.ValidationError(
                'url does not contain a downloadable video resource'
            )
        if not self.is_valid_size(attrs['url']):
            raise serializers.ValidationError(
                'to large video'
            )
        return attrs

    @staticmethod
    def is_downloadable(url):
        """
        Does the url contain a downloadable resource
        """
        h = requests.head(url, allow_redirects=True)
        header = h.headers
        content_type = header.get('content-type')
        if 'video' in content_type.lower():
            return True
        return False

    @staticmethod
    def is_valid_size(url):
        h = requests.head(url, allow_redirects=True)
        header = h.headers
        content_length = header.get('content-length', None)
        if content_length and int(content_length) > settings.MAZ_VIDEO_SIZE:
            return False
        return True
