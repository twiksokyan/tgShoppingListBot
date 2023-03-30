from aiogram import types


async def set_bot_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', 'начать диалог'),
            types.BotCommand('help', 'список доступных команд')
        ]
    )