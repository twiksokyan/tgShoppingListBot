from aiogram import types, Dispatcher


# @rate_limit(5, 'help')
async def bot_help(message: types.Message):
    text = [
        'Список команд: ',
        '/start - Начать диалог',
        '/help - Получить справку'
    ]
    await message.answer('\n'.join(text))


def register_help(dp: Dispatcher):
    dp.register_message_handler(bot_help, commands=['help'])