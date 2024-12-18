from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


async def base_keyb(*args) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    
    for i in args:
        builder.button(
            text=i
        )
    
    return builder.as_markup(resize_keyboard=True)


async def inlines(**kwargs) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for text, cbk_data in kwargs.items():
        builder.button(
            text=text,
            callback_data=cbk_data
        )
    
    return builder.as_markup(resize_keyboard=True)