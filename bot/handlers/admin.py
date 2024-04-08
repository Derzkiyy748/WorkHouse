import asyncio
import time
import config

from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from keyboards.inline.menu import menu_keyboard, menu_profile, menu_o_nas, menu_rules, menu_new_task_1, menu_new_task_2, cancel_task
from aiogram import Bot
from aiogram.types.input_file import FSInputFile
from database.requiests import edit_task, get_task
from states.state import New_task


router_admin = Router()

@router_admin.callback_query(F.data == "yes_task", New_task.chek)
async def yes_task(call: CallbackQuery, bot: Bot, state: FSMContext):

    await call.message.delete()

    us = await state.get_data()

    task = await get_task(us['user_id'])

    await call.answer(text=f"Задание № {task.task_id} добавлено",
                      show_alert=True)
    
    await state.clear()

    await edit_task(us['user_id'])


@router_admin.callback_query(F.data == 'no_task', New_task.chek)
async def yes_task(call: CallbackQuery, bot: Bot, state: FSMContext):

    await call.message.delete()

    us = await state.get_data()

    task = await get_task(us['user_id'])

    await call.answer(text=f"Задание № {task.task_id} удалено",
                      show_alert=True)
    
    await state.clear()




