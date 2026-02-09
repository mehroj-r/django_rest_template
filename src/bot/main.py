from logging import getLogger

from bot.config import get_bot_settings
from bot.runtime import close_bundle, get_bundle

logger = getLogger(__name__)


async def start_polling() -> None:
    bundle = await get_bundle()
    logger.info("Starting bot in polling mode")
    await bundle.dispatcher.start_polling(
        bundle.bot,
        allowed_updates=bundle.dispatcher.resolve_used_update_types(),
    )


async def setup_webhook(drop_pending_updates: bool = False) -> None:
    settings = get_bot_settings()
    bundle = await get_bundle()
    await bundle.bot.set_webhook(
        url=settings.webhook_url,
        secret_token=settings.webhook_secret or None,
        drop_pending_updates=drop_pending_updates,
    )
    logger.info("Webhook configured: %s", settings.webhook_url)


async def remove_webhook(drop_pending_updates: bool = False) -> None:
    bundle = await get_bundle()
    await bundle.bot.delete_webhook(drop_pending_updates=drop_pending_updates)
    logger.info("Webhook deleted")


async def shutdown() -> None:
    await close_bundle()
