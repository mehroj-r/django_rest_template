from django.urls import path

from bot.webhook import views

app_name = "bot_webhook"

urlpatterns = [
    path("webhook/", views.telegram_webhook, name="telegram_webhook"),
]
