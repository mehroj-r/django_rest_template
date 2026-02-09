from aiogram import Router

from bot.routers import setup_routers


def get_root_router() -> Router:
    return setup_routers()
