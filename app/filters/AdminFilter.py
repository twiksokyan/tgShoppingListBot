from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from app.config import admins


class AdminFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        if message.from_user.id in admins:
            return True