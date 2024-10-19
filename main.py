import asyncio
import logging

from aiogram import F, Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters.command import CommandStart
from main_router import router as main_router
from keyboards.main import base_keyb
from classes.user import User


dp = Dispatcher()
dp.include_router(
    main_router
)


@dp.message(CommandStart())
async def go(message: Message):
    if User.instance():
        buttons = ('Дневник', 'Выход', 'Поддержка')
    else:
        buttons = ('Войти', 'Поддержка')
    
    await message.answer(
        text='''
Привет! Это бот "Сетевой Город" в телеграме! Здесь ты можешь получить оценки за неделю.
Бот будет обновляться и в него будут добавляться новые и удобные функции''',
reply_markup=await base_keyb(*buttons)
    )


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot('7249528198:AAFoiK-UvnkgTqtVq21vmCHvCvvLvi6yvo8')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())