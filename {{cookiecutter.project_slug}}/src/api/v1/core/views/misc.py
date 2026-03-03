from rest_framework import generics
from rest_framework.response import Response


class HealthAPIView(generics.RetrieveAPIView):
    permission_classes = []

    def retrieve(self, request, *args, **kwargs):
        return Response(data={"status": "ok"}, status=200)


class TestAPIView(generics.RetrieveAPIView):
    permission_classes = []

    def retrieve(self, request, *args, **kwargs):
        return Response(data={"message": "This is a test endpoint."}, status=200)
