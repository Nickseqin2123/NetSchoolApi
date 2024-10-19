import asyncio
import logging

from aiogram import F, Bot, Dispatcher
from aiogram.types import Message


dp = Dispatcher()


@dp.message()
async def go(message: Message):
    await message.reply(
        text=message.text
    )


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot('7249528198:AAFoiK-UvnkgTqtVq21vmCHvCvvLvi6yvo8')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())