from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

router = Router(name="start")


@router.message(CommandStart())
async def start_handler(message: Message, _):
    await message.answer(_("Welcome to the bot template."))


@router.message(Command("help"))
async def help_handler(message: Message, _):
    help_text = "\n".join(
        [
            _("Available commands:"),
            "/start - " + _("Start bot"),
            "/help - " + _("Show help"),
        ]
    )
    await message.answer(help_text)
