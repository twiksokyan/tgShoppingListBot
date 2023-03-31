from aiogram import Dispatcher

from app.handlers.users.start import register_start
from app.handlers.users.echo import register_echo
from app.handlers.users.help import register_help
from app.handlers.users.shopping_list import register_shopping_list

def register_all_handlers(dp: Dispatcher):
    '''Важен порядок следования хендлеров!!!'''
    register_start(dp)
    register_help(dp)
    register_shopping_list(dp)
    register_echo(dp)
