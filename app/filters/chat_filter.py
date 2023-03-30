from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

from typing import Union


class Private_chat_filter(BoundFilter):
    async def check(self, message: Union[types.Message, types.CallbackQuery]) -> bool:
        if message.chat.type == 'private':
            return True


class Group_chat_filter(BoundFilter):
    async def check(self, message: Union[types.Message, types.CallbackQuery]) -> bool:
        if message.chat.type == 'group':
            return True