from aiogram import Dispatcher
from app.filters.AdminFilter import AdminFilter
from app.filters.chat_filter import Private_chat_filter, Group_chat_filter


def filters_setup(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(Private_chat_filter)
    dp.filters_factory.bind(Group_chat_filter)
