from aiogram import types


async def set_bot_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand('create_list', 'создать список покупок'),
            types.BotCommand('invite', 'пригласить участника в список'),
            types.BotCommand('add', '+ позиция. Добавить позицию в список'),
            types.BotCommand('show_list', 'показать список покупок'),
            types.BotCommand('show_mates', 'показать участников списка'),
            types.BotCommand('quit', 'покинуть текущий список'),
            types.BotCommand('help', 'освежить в памяти правила')
        ]
    )