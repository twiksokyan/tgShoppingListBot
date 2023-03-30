from aiogram import types, Dispatcher

from app.filters.AdminFilter import AdminFilter


async def bot_test(message: types.Message):
    await message.answer(f'Ты @{message.from_user.username} мне написал: {message.text}')


def register_test(dp: Dispatcher):
    dp.register_message_handler(bot_test, AdminFilter(), commands=['test'])