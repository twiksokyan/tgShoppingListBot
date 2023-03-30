from aiogram import Dispatcher

from app.handlers.users.start import register_start
from app.handlers.users.echo import register_echo
from app.handlers.users.help import register_help
from app.handlers.users.test import register_test

def register_all_handlers(dp: Dispatcher):
    '''Важен порядок следования хендлеров!!!'''
    register_start(dp)
    register_help(dp)
    register_test(dp)
    register_echo(dp)
