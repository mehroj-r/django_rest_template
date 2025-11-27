from django.urls import path

from core.api.views.misc import HealthAPIView

app_name = "health"

urlpatterns = [
    path("", HealthAPIView.as_view(), name="health-api"),
]
