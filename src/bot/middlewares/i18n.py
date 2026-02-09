from aiogram import BaseMiddleware

from bot.etc.container import Container


class I18nMiddleware(BaseMiddleware):
    def __init__(self, container: Container):
        self.container = container

    async def __call__(self, handler, event, data):
        user = data.get("event_from_user")
        locale = (
            getattr(user, "language_code", None)
            or self.container.settings.default_locale
            or self.container.settings.fallback_locale
        )
        data["locale"] = locale
        data["_"] = self.container.translator.gettext(locale)
        return await handler(event, data)
