from django.urls import path

from api.v1.core.views.misc import HealthAPIView

app_name = "misc"

urlpatterns = [
    path("health/", HealthAPIView.as_view(), name="health-api"),
]
