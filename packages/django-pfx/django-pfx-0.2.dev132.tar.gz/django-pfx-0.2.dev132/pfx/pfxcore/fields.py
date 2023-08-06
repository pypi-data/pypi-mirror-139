import logging

from django.db import models

from pfx.pfxcore.storage import DefaultStorage

logger = logging.getLogger(__name__)


class MediaField(models.JSONField):
    def __init__(
            self, *args, max_length=255, get_key=None, storage=None,
            **kwargs):
        self.get_key = get_key or self.get_default_key
        self.storage = storage or DefaultStorage()
        super().__init__(
            *args, max_length=max_length,
            default=kwargs.pop('default', dict),
            blank=kwargs.pop('blank', True),
            **kwargs)

    @staticmethod
    def get_default_key(obj, filename):
        return f"{type(obj).__name__}/{obj.pk}/{filename}"

    def to_python(self, value):
        return super().to_python(self.storage.to_python(value))

    def get_upload_url(self, request, obj, filename):
        key = self.get_key(obj, filename)
        url = self.storage.get_upload_url(request, key)
        return dict(url=url, file=dict(name=filename, key=key))

    def get_url(self, request, obj):
        return self.storage.get_url(
            request, self.value_from_object(obj)['key'])
