from logging import getLogger

from bot.config import BotSettings
from bot.etc.translator import Translator

logger = getLogger(__name__)


class Container:
    def __init__(self, settings: BotSettings):
        self.settings = settings
        self.logger = logger
        self.translator = Translator(
            locales_path=settings.locales_path,
            fallback_locale=settings.fallback_locale,
        )
