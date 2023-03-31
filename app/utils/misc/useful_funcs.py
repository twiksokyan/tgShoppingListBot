from app.config import admins
from app.loader import db, dp


def choose_user_name(user_full_name_dict):
    if user_full_name_dict['tg_username']:
        return f'@{user_full_name_dict["tg_username"]}'
    elif user_full_name_dict['full_name']:
        return user_full_name_dict['full_name']
    else:
        return 'Unknown User'

async def get_list_users(tg_id):
    """Забирает всех пользователей списка, кроме чувака из аргумента функции"""
    users_in_list = await db.get_list_users(tg_id=tg_id)
    users_in_list_for_text = []
    for user in users_in_list:
        user_name = choose_user_name(dict(user))
        users_in_list_for_text.append(user_name)
    return ', '.join(users_in_list_for_text)

async def send_message_to_admin(text):
    for admin in admins:
        await dp.bot.send_message(
            chat_id=admin,
            text=text
        )