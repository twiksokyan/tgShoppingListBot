import asyncpg
from aiogram import types, Dispatcher

from app.config import admins
from app.filters.chat_filter import Private_chat_filter
from app.loader import db, dp


async def bot_start(message: types.Message):
    try:
        username = message.from_user.username if message.from_user.username else 'unknown'
        fullname = message.from_user.full_name if message.from_user.full_name else 'Unnamed Unlastnamed'
        # user = await db.add_user(tg_id=message.from_user.id,
        #                          tg_username=username,
        #                          full_name=fullname)
        # user_dict = dict(user)

        answer_text = '\n'.join([
            f'Приветик, {fullname}!',
            f'',
            f'Пукни в пакетик'
        ])
        await message.answer(answer_text)

        # message_to_admin_text = '\n'.join([
        #     f'Новый пользователь',
        #     f'<b>USERNAME:</b> <code>{user_dict["tg_username"]}</code>',
        #     f'<b>FULLNAME:</b> <code>{user_dict["full_name"]}</code>',
        #     f'<b>TELEGRAM_ID:</b> <code>{user_dict["tg_id"]}</code>',
        #     f'Добавлен в БД.'
        # ])
        # await dp.bot.send_message(
        #     chat_id=admins[0],
        #     text=message_to_admin_text
        # )
    except asyncpg.exceptions.UniqueViolationError:
        await message.answer('Приветик!\n\nПукни в пакетик')


def register_start(dp: Dispatcher):
    dp.register_message_handler(bot_start, Private_chat_filter, commands=['start'])