import os
from aiogram import F, Router
from aiogram.utils.chat_action import ChatActionSender
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.main import base_keyb
from classes.user import User
from other.utils import schools_in_region
from other.middlewares import SchoolMiddlware


router = Router(name=__name__)
router.message.middleware(SchoolMiddlware())


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
        schools = await schools_in_region(message.text, message.from_user.id)
        await state.update_data(schools=schools)
    except Exception:
        await message.answer(
            text='Вы ввели не корректный URL! Введите корректный URL или обратитесь в поддержку'
        )
        await state.set_state(UserForm.url)
    else:
        await state.set_state(UserForm.school)
        
        async with ChatActionSender.upload_document(chat_id=message.chat.id, bot=message.bot):
            await message.bot.send_document(
                chat_id=message.chat.id,
                document=FSInputFile(f'{message.from_user.id}.txt')
                )
        os.remove(f'{message.from_user.id}.txt')
            
        await message.answer(
            text='''
Отлично, теперь введи свою школу из файла. В файле все школы твоего региона.
Копируй школу полностью без изменений!'''
        )
        

@router.message(UserForm.school)
async def get_school(message: Message, state: FSMContext, school: str):
    state_data = await state.get_data()
    
    await message.answer(
        text=school
    )
        
    for school in state_data['schools']:
        if school['shortName'] == message.text:
            break
        await state.update_data(school=school)
    else:
        await message.answer(
            text='Вы ввели не корректную школу. Введите школу корректно!'
        )
        await state.set_state(UserForm.school)