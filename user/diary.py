from typing import Coroutine

from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from classes.user import User
from keyboards.main import base_keyb, inlines
from diaryoperation.diary import convert_and_set_in_dict, diary_print


router = Router(name=__name__)


class DateForm(StatesGroup):
    start = State()


@router.message(F.text == 'Дневник', F.func(lambda _: User.instance()))
async def diary(message: Message) -> Coroutine:
    await message.answer(
        text='Мы в дневнике',
        reply_markup=ReplyKeyboardRemove()
    )
    
    await message.answer(
        text='Вы хотите получить дневник за эту неделю?',
        reply_markup=await inlines(Да='Да', Нет='Нет')
    )
    

@router.callback_query(F.data == 'Да')
async def callback_yes(callback: CallbackQuery) -> Coroutine:
    await callback.message.delete()
    user = User()
    diary: dict = await user.diary()
    finall_data = await convert_and_set_in_dict(diary['message']['weekDays'])
    
    async for day in diary_print(finall_data):
        await callback.message.answer(
            text=day
        )
    
    await callback.message.answer(
        text='Выдача окончена',
        reply_markup=await base_keyb('Дневник', 'Выход', 'Поддержка')
    )
        

@router.callback_query(F.data == 'Нет')
async def callback_yes(callback: CallbackQuery, state: FSMContext) -> Coroutine:
    await callback.message.delete()
    await state.set_state(DateForm.start)
    
    await callback.message.answer(
        text='Укажите начало недели для просмотра дневника за всю неделю. Формат даты "Год-Месяц-День". Указывать через "-"',
        reply_markup=await base_keyb('Главное меню')
    )

    
@router.message(F.text == 'Главное меню')
async def main_menu(message: Message, state: FSMContext) -> Coroutine|None:
    current_state = await state.get_state()
    
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        text='Мы в менюшечке',
        reply_markup=await base_keyb('Дневник', 'Выход', 'Поддержка')
    )


@router.message(DateForm.start)
async def get_start(message: Message, state: FSMContext) -> Coroutine:
    try:
        datetime.strptime(message.text, "%Y-%m-%d")
    except Exception:
        await state.set_state(DateForm.start)
        await message.answer(
            text='Не верный формат даты!'
        )
        await message.answer(
        text='Укажите начало недели для просмотра дневника за всю неделю. Формат даты "Год-Месяц-День". Указывать через "-"'
    )
        
    else:
        await state.update_data(start=message.text)
        
        data: dict = await state.get_data()
        await state.clear()
        
        await summary(message, state, data)


async def summary(message: Message, state: FSMContext, data: dict) -> Coroutine:
    user = User()
    diary: dict = await user.diary(data['start'])
    
    if diary['status']:
    
        finall_data = await convert_and_set_in_dict(diary['message']['weekDays'])
        
        
        async for day in diary_print(finall_data):
            await message.answer(
                text=day
            )
        
        await message.answer(
            text='Выдача окончена',
            reply_markup=await base_keyb('Дневник', 'Выход', 'Поддержка')
        )
    else:
        await message.answer(
            text=diary['message'],
            reply_markup=await base_keyb('Дневник', 'Выход', 'Поддержка')
        )