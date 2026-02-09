from aiogram import Router

from bot.routers import fallback, start


def setup_routers() -> Router:
    root = Router(name="root")
    root.include_router(start.router)
    root.include_router(fallback.router)
    return root
