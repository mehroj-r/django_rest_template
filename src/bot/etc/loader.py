from dataclasses import dataclass

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import get_bot_settings
from bot.etc.container import Container
from bot.middlewares import DIMiddleware
from bot.middlewares import ErrorMiddleware
from bot.middlewares import I18nMiddleware
from bot.url_router import get_root_router


@dataclass
class BotBundle:
    bot: Bot
    dispatcher: Dispatcher
    container: Container


def create_bot_bundle() -> BotBundle:
    settings = get_bot_settings()
    parse_mode_key = settings.parse_mode.strip().upper().replace("-", "_")
    parse_mode_key = "MARKDOWN_V2" if parse_mode_key == "MARKDOWNV2" else parse_mode_key
    parse_mode = ParseMode.__members__.get(parse_mode_key, ParseMode.HTML)
    bot = Bot(token=settings.token, default=DefaultBotProperties(parse_mode=parse_mode))
    container = Container(settings=settings)

    dispatcher = Dispatcher(storage=MemoryStorage())
    dispatcher.update.outer_middleware(ErrorMiddleware())
    dispatcher.update.middleware(I18nMiddleware(container=container))
    dispatcher.update.middleware(DIMiddleware(container=container))
    dispatcher.include_router(get_root_router())

    return BotBundle(bot=bot, dispatcher=dispatcher, container=container)
