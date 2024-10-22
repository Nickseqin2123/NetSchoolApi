from typing import Coroutine

from aiogram import Router, F
from aiogram.types import Message
from classes.user import User


router = Router(name=__name__)


@router.message(F.text == 'Выход', F.func(lambda _: User.instance()))
async def logout(message: Message) -> Coroutine:
    user = User()

    if user._session.closed:
        await message.answer(
            text='У вас не активных сессий'
        )
    else:  
        await user.logout()
        await message.answer(
            text='Сессия завершена'
        )