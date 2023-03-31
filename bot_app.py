from aiogram import executor, Dispatcher

from app.filters.filters_setup import filters_setup
from app.utils.notify_admins import on_startup_notify
from app.utils.set_commands import set_bot_commands
from app.loader import dp, db
from app.handlers.register_handlers import register_all_handlers
from app.utils.misc import logging


async def on_startup(dp: Dispatcher):
    logging.info('Create connection to DB db_shopping_list_bot')
    await db.create_connection()

    logging.info('Create table USERS')
    await db.create_table_users()
    logging.info('Create table USERS_LISTS')
    await db.create_table_users_lists()
    logging.info('Create table SHOPPING_LISTS')
    await db.create_table_shopping_lists()

    logging.info('Done!')

    register_all_handlers(dp)
    filters_setup(dp)

    await on_startup_notify(dp)
    await set_bot_commands(dp)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)