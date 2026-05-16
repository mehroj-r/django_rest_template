from core.api.views import BaseAPIView
from rest_framework.response import Response


class HealthAPIView(BaseAPIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        return Response(data={"status": "ok"}, status=200)


class TestAPIView(BaseAPIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        return Response(data={"message": "This is a test endpoint."}, status=200)
