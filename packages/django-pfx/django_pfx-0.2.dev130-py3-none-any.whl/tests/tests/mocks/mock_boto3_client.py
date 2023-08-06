import logging

logger = logging.getLogger(__name__)


class MockBoto3Client:
    def generate_presigned_url(self, *args, **kwargs):
        params = kwargs.get('Params', {})
        return f"http://{params.get('Bucket')}/{params.get('Key')}"

    def head_object(self, *args, **kwargs):
        return dict(ContentLength=1000, ContentType="image/png")
