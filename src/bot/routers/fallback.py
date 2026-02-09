from aiogram import F, Router
from aiogram.types import Message

router = Router(name="fallback")


@router.message(F.text, F.text.startswith("/"))
async def unknown_command_handler(message: Message, _):
    await message.answer(_("Unknown command. Use /help."))
