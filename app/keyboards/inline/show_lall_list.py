from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from app.loader import db


items_cd = CallbackData('item', 'item_id')

def generate_items_cd(item_id):
    return items_cd.new(item_id=item_id)


async def generate_items_list(list_id):
    keyboard = InlineKeyboardMarkup(row_width=1)

    items_list = await db.get_all_list(list_id=list_id)
    if items_list:
        for item in items_list:
            item_dict = dict(item)
            button_text = f'{item_dict["item_nm"]}'
            current_cd = generate_items_cd(item_dict["item_id"])
            keyboard.insert(
                InlineKeyboardButton(
                    text=button_text,
                    callback_data=current_cd
                )
            )
        keyboard.row(
            InlineKeyboardButton(
                text='Удалить ФСЁ!',
                callback_data='delete'
            )
        )

    return keyboard