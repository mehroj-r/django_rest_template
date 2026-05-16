from core.api.views import BaseAPIView


class HealthAPIView(BaseAPIView):
    auth = ()

    def get(self):
        return {"status": "ok"}


class TestAPIView(BaseAPIView):
    auth = ()

    def get(self):
        return {"message": "This is a test endpoint."}
