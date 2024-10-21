import requests
from aiogram import Router, F
from aiogram.types import Message
from classes.user import User


router = Router(name=__name__)


@router.message(F.text == 'Выход', F.func(lambda _: User.instance()))
async def logout(message: Message):
    user = User()

    try:
        user._session.get('https://example.com')
    except requests.exceptions.RequestException:
        await message.answer(
            text='У вас не активных сессий'
        )
    else:  
        user.logout()
        await message.answer(
            text='Сессия завершена'
        )