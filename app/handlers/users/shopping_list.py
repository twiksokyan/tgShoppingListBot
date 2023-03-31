from aiogram import types, Dispatcher

from app.keyboards.inline.show_lall_list import generate_items_list, items_cd
from app.loader import db, dp
from app.filters.chat_filter import Private_chat_filter
from app.utils.misc import useful_funcs


async def create_new_list(message: types.Message):
    """Создание нового списка по команде create_list"""
    is_user_already_in_list = await db.count_user_lists(tg_id=message.from_user.id)
    # проверка на наличие списка у пользователя
    if not is_user_already_in_list:
        new_list = await  db.add_new_list(tg_id=message.from_user.id)
        new_list_dict = dict(new_list)

        await message.answer(
            text='\n'.join([
                f'Ты создал новый список!🥳',
                f'',
                f'По моей идеологии, чтобы начать пользоваться списком, тебе надо пригласить'
                f' человека или людей, с кем ты планируешь составлять общий список покупок.',
                f'Для этого воспользуйся командой <code>/invite</code>.',
                f'',
                f'Полученное после команды <code>/invite</code> сообщение перешли тому, кого хочешь пригласить присоединиться к общему списку покупок.'
            ])
        )
        #уведомляем админа
        text_for_admin = '\n'.join([
            f'Пользователь',
            f'<b>TELEGRAM_ID:</b> <code>{new_list_dict["tg_id"]}</code>',
            f'Создал новый список',
            f'<b>LIST_ID:</b> <code>{new_list_dict["list_id"]}</code>'
        ])
        await useful_funcs.send_message_to_admin(text_for_admin)
    else:
        # достаем всех пользователей списка, кроме приглашенного
        users_in_list_text = await useful_funcs.get_list_users(tg_id=message.from_user.id)
        if users_in_list_text:
            answer_part = f'уже состоишь в списке с {users_in_list_text}.\n' \
                          f'Для выхода их списка воспользуйся командой <code>/quit</code>'
        else:
            answer_part = 'уже состоишь в списке, где ты — единственный участник.\n' \
                          'Можешь выйти командой <code>/quit</code>' \
                          ' или пригласить новых участников командой <code>/invite</code>'
        await message.answer(
            text='\n'.join([
                'Не могу создать список для тебя😔',
                f'❗Ты {answer_part}'
            ])
        )


async def invite_mate(message: types.Message):
    """Генерация сообщения для приглашения близкого в список по команде /invite"""
    is_inviter_in_list = await db.count_user_lists(tg_id=message.from_user.id)

    if is_inviter_in_list:
        bot = await dp.bot.get_me()
        inviter = useful_funcs.choose_user_name(
            {
                'tg_username': message.from_user.username,
                'full_name': message.from_user.full_name
            }
        )
        await message.answer(text='\n'.join([
            f'Привет!👋🏼',
            f'📩Приглашаю тебя присоединиться к общему списку покупок с {inviter}.',
            f'',
            f'Для этого тебе нужно перейти в личные сообщения со мной @{bot.username}'
            f' и после начала диалога отправить команду (скопируй команду быстрым нажатием):',
            f'',
            f'<code>/join {message.from_user.id}</code>'
        ]))
    else:
        await message.answer(
            text='\n'.join([
                '❗Ты не можешь приглашать пользователей, так как сам не состоишь в списке😔',
                'Можешь создать список <code>/create_list</code> и потом отправить инвайты.'
            ])
        )


async def join_to_list(message: types.Message):
    """Присоединение к списку по команде /join <tg_id_of_inviter> с аргументом"""
    message_args = message.get_args()
    if not message_args:
        await message.answer(
            '❗Для присоединения к совместному списку покупок, запроси инвайт.'
        )
    else:
        try:
            inviter_id = int(message_args)
        except ValueError:
            inviter_id = -1

        if inviter_id == message.from_user.id:
            #когда создатель списка хочет добавиться сам к себе
            await message.answer('Хочешь вести общий список покупок с самим собой, Билли Миллиган?😏')
        else:
            # проверка на id пользователя, к которому хотят присоединиться
            is_inviter_has_list = await db.count_user_lists(tg_id=inviter_id)
            if is_inviter_has_list: #если inviter состоит в списке
                #проверяем, есть приглашенный пользователь в каком-нибудь списке
                is_user_already_in_list = await db.count_user_lists(message.from_user.id)
                if not is_user_already_in_list:
                    #забираем list_id на основе inviter'а
                    list_id = await db.get_list_id(tg_id=inviter_id)
                    invited_user = await db.add_user_to_list(
                        tg_id=message.from_user.id,
                        list_id=list_id
                    )
                    # достаем всех пользователей списка, кроме вновь добавленного
                    users_in_list_text = await useful_funcs.get_list_users(tg_id=message.from_user.id)

                    await message.answer(
                        text='\n'.join([
                            f'Отлично!🥳',
                            f' Теперь ты можешь добавлять необходимые позиции в общий список покупок с '
                            f'{users_in_list_text}.',
                            f'Для добавления позиции воспользуйся командой <code>/add *name*</code>, где <code>*name*</code>'
                            f' замени на название позиции.',
                            f'Например <code>/add молоко</code>'
                        ])
                    )
                    #рассылкаем друзьям уведомление о присоединении нового человека
                    users_in_list = await db.get_list_users(tg_id=message.from_user.id)
                    new_user_name = useful_funcs.choose_user_name(
                        {
                            'tg_username': message.from_user.username,
                            'full_name': message.from_user.full_name
                        }
                    )
                    for user in users_in_list:
                        user_dict = dict(user)
                        await dp.bot.send_message(
                            chat_id=user_dict["tg_id"],
                            text=f'😍{new_user_name} присоединился!'
                        )
                    # уведомляем админа
                    text_for_admin = '\n'.join([
                        f'Пользователь',
                        f'<b>TELEGRAM_ID:</b> <code>{invited_user["tg_id"]}</code>',
                        f'Добавлен в список',
                        f'<b>LIST_ID:</b> <code>{invited_user["list_id"]}</code>'
                    ])
                    await useful_funcs.send_message_to_admin(text_for_admin)
                else: # если чувак/чувиха уже в списке
                    # достаем всех пользователей списка, кроме приглашенного
                    users_in_list_text = await useful_funcs.get_list_users(tg_id=message.from_user.id)
                    if users_in_list_text:
                        answer_part = f'👨‍👩‍👧‍👦Ты уже состоишь в общем списке покупок с {users_in_list_text}.'
                    else:
                        answer_part = 'Ты состоишь в списке покупок, но с тобой тут никого нет🙁'
                    await message.answer(
                        text='\n'.join([
                            f'{answer_part}',
                            f'❗Нельзя состоять в нескольких списках одновременно.',
                            f'Для выхода из текущего списка воспользуйся командой <code>/quit</code>'
                        ])
                    )
            else: # если аргумент-список покупок неверный
                await message.answer('❗Такого общего списка покупок не существует.')


async def quit_from_list(message: types.Message):
    is_user_in_list = await db.count_user_lists(tg_id=message.from_user.id)
    #если чувак/чувиха есть в списке
    if is_user_in_list:
        users_in_list = await db.get_list_users(tg_id=message.from_user.id)
        quit_user = await db.delete_user_from_list(tg_id=message.from_user.id)
        quit_user_dict = dict(quit_user)

        await message.answer(
            text='\n'.join([
                '✔Ты успешно вышел из списка!',
                'Если ты сделал это по ошибке, попроси прислать тебе повторный инвайт.'
            ])
        )
        # определяем имя вышедшего пользователя и уведомляем друзей
        quit_user_name = useful_funcs.choose_user_name(
            {
                'tg_username': message.from_user.username,
                'full_name': message.from_user.full_name
            }
        )
        for user in users_in_list:
            user_dict = dict(user)
            await dp.bot.send_message(
                chat_id=user_dict["tg_id"],
                text=f'😭{quit_user_name} покинул вас..'
            )
        #уведомляем админа
        text_for_admin = '\n'.join([
            f'Пользователь',
            f'<b>TELEGRAM_ID:</b> <code>{quit_user_dict["tg_id"]}</code>',
            f'Вышел из списка',
            f'<b>LIST_ID: </b> <code>{quit_user_dict["list_id"]}</code>'
        ])
        await useful_funcs.send_message_to_admin(text_for_admin)
    else:
        await message.answer('❗Ты и так не состоишь в списке.')


async def show_list_participants(message: types.Message):
    """Для просмотре состава списка"""
    is_user_in_list = await db.count_user_lists(tg_id=message.from_user.id)
    if is_user_in_list:
        users_in_list_text = await useful_funcs.get_list_users(tg_id=message.from_user.id)
        if users_in_list_text:
            answer_text = f'👨‍👩‍👧‍👦Ты состоишь в списке с {users_in_list_text}.'
        else:
            answer_text = '❗Ты — единственный участник списка.'
    else:
        answer_text = '❗Ты не состоишь в списке.'
    await message.answer(text=answer_text)


async def add_item(message: types.Message):
    is_user_in_list = await db.count_user_lists(tg_id=message.from_user.id)
    if is_user_in_list:
        items = message.get_args().split()
        if items:
            list_id = await db.get_list_id(tg_id=message.from_user.id)
            added_items = []
            for item_nm in items:
                added_item = await db.add_item(list_id=list_id, item_nm=item_nm)
                item_dict = dict(added_item)
                added_items.append(item_dict['item_nm'])
            added_items_text = '\n  ▫'.join(added_items)
            await message.answer(
                text=f'➕Добавлено в список:\n'
                     f'  ▫{added_items_text}'
            )
        else:
            await message.answer(
                text='\n'.join([
                    '❗Для добавления позиций в список, необходимо перечислить их <b><u>через пробел</u></b> '
                    'после команды <code>/add</code>.',
                    'Например: <code>/add молоко хлеб пивко</code>'
                ])
            )
    else:
        await message.answer('❗Ты не состоишь в списке, добавить позицию не получится.')

@dp.callback_query_handler(items_cd.filter())
async def delete_item(call: types.CallbackQuery, callback_data: dict):
    try:
        deleted_item = await db.delete_item(item_id=int(callback_data.get('item_id')))
        deleted_item_dict = dict(deleted_item)
        await call.answer(
            text=f'➖Удалено из списка: {deleted_item_dict["item_nm"]}',
            show_alert=True,
            cache_time=10
        )

        updated_reply_markup = await generate_items_list(list_id=deleted_item_dict["list_id"])
        if updated_reply_markup.inline_keyboard:
            await call.message.edit_reply_markup(updated_reply_markup)
        else:
            await call.message.edit_text('🛒Список покупок пуст.')
    except TypeError:
        await call.answer(
            text='➖Эта позиция уже удалена',
            show_alert=True,
            cache_time=10
        )
        list_id = await db.get_list_id(tg_id=call.from_user.id)
        updated_reply_markup = await generate_items_list(list_id=list_id)
        if updated_reply_markup.inline_keyboard:
            await call.message.edit_reply_markup(updated_reply_markup)
        else:
            await call.message.edit_text('🛒Список покупок пуст.')


@dp.callback_query_handler(text='delete')
async def delete_all_list(call: types.CallbackQuery):
    list_id = await db.get_list_id(tg_id=call.from_user.id)
    await db.clear_shopping_list(list_id=list_id)

    await call.answer(
        text='❗Список покупок полностью очищен.',
        show_alert=True,
        cache_time=10
    )

    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.edit_text('🛒Список покупок пуст.')



async def show_list(message: types.Message):
    is_user_in_list = await db.count_user_lists(tg_id=message.from_user.id)
    if is_user_in_list:
        list_id = await db.get_list_id(tg_id=message.from_user.id)
        reply_markup = await generate_items_list(list_id=list_id)
        if reply_markup.inline_keyboard:
            await message.answer(
                text='🧾Список покупок:',
                reply_markup=reply_markup
            )
        else:
            await message.answer('🛒Список покупок пуст.')
    else:
        await message.answer('❗Ты не состоишь в списке.')

def register_shopping_list(dp: Dispatcher):
    dp.register_message_handler(create_new_list, commands=['create_list'])
    dp.register_message_handler(invite_mate, Private_chat_filter() ,commands=['invite'])
    dp.register_message_handler(join_to_list, Private_chat_filter(), commands=['join'])
    dp.register_message_handler(quit_from_list, Private_chat_filter(), commands=['quit'])
    dp.register_message_handler(show_list_participants, commands=['show_mates'])
    dp.register_message_handler(add_item, commands=['add'])
    dp.register_message_handler(show_list, commands=['show_list'])