import json

from aiogram.types import Update
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from bot.config import get_bot_settings
from bot.runtime import get_bundle


@csrf_exempt
async def telegram_webhook(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    settings = get_bot_settings()
    if settings.mode != "webhook":
        return JsonResponse({"detail": "Webhook mode is disabled"}, status=404)

    secret_header = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
    if settings.webhook_secret and secret_header != settings.webhook_secret:
        return JsonResponse({"detail": "Invalid secret"}, status=403)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"detail": "Invalid JSON payload"}, status=400)

    bundle = await get_bundle()
    update = Update.model_validate(payload, context={"bot": bundle.bot})
    await bundle.dispatcher.feed_update(bundle.bot, update)
    return JsonResponse({"ok": True})
