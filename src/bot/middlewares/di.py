from aiogram import BaseMiddleware

from bot.etc.container import Container


class DIMiddleware(BaseMiddleware):
    def __init__(self, container: Container):
        self.container = container

    async def __call__(self, handler, event, data):
        data["container"] = self.container
        return await handler(event, data)
