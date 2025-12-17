from django.urls import path

from api.v1.core.views.misc import HealthAPIView, TestAPIView

app_name = "misc"

urlpatterns = [
    path("health/", HealthAPIView.as_view(), name="health-api"),
    path("test/", TestAPIView.as_view(), name="test-api"),
]
