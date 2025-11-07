from django.urls import path

from apps.core.api.views import HealthAPIView

app_name = "health"

urlpatterns = [
    path("", HealthAPIView.as_view(), name="health-api"),
]
