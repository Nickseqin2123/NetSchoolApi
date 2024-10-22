from typing import Coroutine

from aiogram import Router, F
from aiogram.types import Message


router = Router(name=__name__)


@router.message(F.text == 'Поддержка')
async def support(message: Message) -> Coroutine:
    await message.answer(
        text='Заметили проблему? Обратитесь по юзу: @Yorichi993'
    )