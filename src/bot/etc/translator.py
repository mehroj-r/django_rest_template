import gettext
from functools import lru_cache
from pathlib import Path
from typing import Callable


class Translator:
    def __init__(
        self, locales_path: Path, domain: str = "bot", fallback_locale: str = "en"
    ):
        self.locales_path = locales_path
        self.domain = domain
        self.fallback_locale = fallback_locale

    @lru_cache(maxsize=32)
    def _translation(self, locale: str) -> gettext.NullTranslations:
        return gettext.translation(
            self.domain,
            localedir=str(self.locales_path),
            languages=[locale],
            fallback=True,
        )

    def gettext(self, locale: str) -> Callable[[str], str]:
        translation = self._translation(locale or self.fallback_locale)
        return translation.gettext
