from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def base_keyb(*args):
    builder = ReplyKeyboardBuilder()
    
    for i in args:
        builder.button(
            text=i
        )
    
    return builder.as_markup(resize_keyboard=True)