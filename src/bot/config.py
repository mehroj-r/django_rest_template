from dataclasses import dataclass
from pathlib import Path

from django.conf import settings


@dataclass(frozen=True)
class BotSettings:
    token: str
    mode: str
    webhook_base_url: str
    webhook_path: str
    webhook_secret: str
    parse_mode: str
    default_locale: str
    fallback_locale: str
    locales_path: Path

    @property
    def webhook_url(self) -> str:
        base = self.webhook_base_url.rstrip("/")
        path = self.webhook_path if self.webhook_path.startswith("/") else f"/{self.webhook_path}"
        return f"{base}{path}"


def get_bot_settings() -> BotSettings:
    return BotSettings(
        token=settings.BOT_TOKEN,
        mode=settings.BOT_MODE,
        webhook_base_url=settings.BOT_WEBHOOK_BASE_URL,
        webhook_path=settings.BOT_WEBHOOK_PATH,
        webhook_secret=settings.BOT_WEBHOOK_SECRET,
        parse_mode=settings.BOT_PARSE_MODE,
        default_locale=settings.BOT_DEFAULT_LOCALE,
        fallback_locale=settings.BOT_FALLBACK_LOCALE,
        locales_path=settings.LOCALE_PATHS,
    )
