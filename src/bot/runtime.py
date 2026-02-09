import asyncio

from bot.etc.loader import BotBundle, create_bot_bundle

_bundle: BotBundle | None = None
_lock = asyncio.Lock()


async def get_bundle() -> BotBundle:
    global _bundle
    if _bundle is not None:
        return _bundle

    async with _lock:
        if _bundle is None:
            _bundle = create_bot_bundle()
    return _bundle


async def close_bundle() -> None:
    global _bundle
    if _bundle is None:
        return
    await _bundle.bot.session.close()
    _bundle = None
