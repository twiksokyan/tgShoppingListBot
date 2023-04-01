from aiogram import types, Dispatcher


async def bot_echo(message: types.Message):
    # print(message.text)
    # await message.answer(message.text)
    pass

def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo)