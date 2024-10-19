import os
from aiogram import F, Router
from aiogram.utils.chat_action import ChatActionSender
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.main import base_keyb
from classes.user import User
from other.utils import schools_in_region


router = Router(name=__name__)


class UserForm(StatesGroup):
    url = State()
    school = State()
    login = State()
    password = State()


@router.message(F.text == 'Войти', F.func(lambda _: User.instance() is False))
async def start_login(message: Message, state: FSMContext):
    await state.set_state(UserForm.url)
    await message.answer(
        text='Так, для начала введи URL сайта сетевого города без последнего символа "/"',
        reply_markup=await base_keyb('Главное меню')
    )


@router.message(F.text == 'Главное меню')
async def main_menu(message: Message, state: FSMContext):
    current_state = await state.get_state()
    
    if current_state is None:
        return
    
    await state.clear()
    
    await message.answer(
        text='Мы в меню',
        reply_markup=await base_keyb('Вход', 'Поддержка')
    )


@router.message(UserForm.url)
async def url_get(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    
    try:
        await schools_in_region(message.text, message.from_user.id)
    except Exception:
        await message.answer(
            text='Вы ввели не корректный URL! Введите корректный URL или обратитесь в поддержку'
        )
        await state.set_state(UserForm.url)
    else:
        async with ChatActionSender.upload_document(chat_id=message.chat.id, bot=message.bot):
            await message.bot.send_document(
                chat_id=message.chat.id,
                document=FSInputFile(f'{message.from_user.id}.txt')
                )
            
        await message.answer(
            text='''
Отлично, теперь введи свою школу из файла которые доступны в твоём регионе.
Копируй школу полностью без изменений!'''
        )
    await state.set_state(UserForm.school)
    os.remove(f'{message.from_user.id}.txt')