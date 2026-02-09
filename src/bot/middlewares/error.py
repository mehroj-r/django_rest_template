from logging import getLogger
from typing import TYPE_CHECKING, Optional

from aiogram import BaseMiddleware

logger = getLogger(__name__)

if TYPE_CHECKING:
    from aiogram.types import Message, CallbackQuery


class ErrorMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):

        try:
            return await handler(event, data)
        except Exception as e:
            logger.exception(f"Unhandled bot exception: {e}")

            message = self._get_message(event)

            if message:
                translate = data.get("_", lambda x: x)
                await message.answer(
                    translate("Something went wrong. Please try again later.")
                )

            return None

    @staticmethod
    def _get_message(event) -> Optional["Message"]:
        from aiogram.types import Message, CallbackQuery

        if isinstance(event, Message):
            return event
        elif isinstance(event, CallbackQuery):
            return event.message
        return None
