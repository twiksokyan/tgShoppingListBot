from aiogram import executor, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.filters.filters_setup import filters_setup
from app.utils.notify_admins import on_startup_notify
from app.utils.set_commands import set_bot_commands
from app.loader import dp
from app.handlers.register_handlers import register_all_handlers
from app.utils.misc import logging
from app.middlewares.scheduler import SchedulerMiddleware


async def on_startup(dp: Dispatcher):
    register_all_handlers(dp)
    filters_setup(dp)

    scheduler = AsyncIOScheduler()
    dp.setup_middleware(SchedulerMiddleware(scheduler))
    scheduler.start()


    await on_startup_notify(dp)
    await set_bot_commands(dp)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)