from debug_toolbar.toolbar import debug_toolbar_urls
from django.urls import path, include

urlpatterns = [
    path('api-auth/', include('rest_framework.urls'))
] + debug_toolbar_urls()