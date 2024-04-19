import asyncio
import time
import config

from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, ReplyKeyboardRemove
from keyboards.inline.menu import  cancel_task, accept
from keyboards.inline.admin import main_menu_admin, finish_addchat
from aiogram import Bot
from aiogram.types.input_file import FSInputFile
from database.requiests import full_add_task, get_task, delete_task, add_chat

from misc.message import (
                            channel_task
                        )

from fliters.Fliter import Admin
from states.state import AddChats


router_admin = Router()


@router_admin.callback_query(F.data == 'admin')
async def admin(call: CallbackQuery, bot: Bot):
    await bot.edit_message_media(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        media=InputMediaPhoto(
                            media=FSInputFile(path="bot/images/kross.jpg"),
                            caption="Админ-панель"
                        ),
                        reply_markup= await main_menu_admin()
                    )

@router_admin.callback_query(F.data.startswith("yestask_"), Admin())
async def yes_task(call: CallbackQuery, bot: Bot):

    await call.message.delete()

    task_id = call.data.split("_")[1]

    task = await get_task(task_id)

    await full_add_task(task_id)

    await call.answer(text=f"✔️Задание № {task.task_id} добавлено",
                      show_alert=True)
    await bot.send_message(chat_id=task.user_id_task, text=f"✔️Ваше задание № {task.task_id} добавлено")
    
    await bot.send_message(chat_id=config.group_task, 
                           text=channel_task(task), 
                           reply_markup=await accept(str(task.task_id)), parse_mode='html')
    
    

@router_admin.callback_query(F.data.startswith("notask_"), Admin())
async def yes_task(call: CallbackQuery, bot: Bot):

    await call.message.delete()

    task_id = call.data.split("_")[1]

    task = await get_task(task_id)

    await call.answer(text=f"❌Задание № {task.task_id} удалено",
                      show_alert=True)
    
    await bot.send_message(chat_id=task.user_id_task, text=f"❌ Ваше задание № {task.task_id} удалено\nК сожалению, оно не прошло модерацию..")
    
    await delete_task(task_id)


@router_admin.callback_query(F.data == 'add_chat')
async def add_chat_1(call: CallbackQuery, state: FSMContext):
    await call.message.answer(text="Введите ID чата и ссылку приглашения\nформат:\nid:ссылка", reply_markup=await finish_addchat())
    await state.set_state(AddChats.add_chats)


@router_admin.message(AddChats.add_chats)
async def add_chat_2(message: Message, state: FSMContext):

    if message.text == "Отмена":
        await message.answer(text="Вы отменили загрузку чатов", reply_markup=ReplyKeyboardRemove())
        await state.clear()
        return

    dat = message.text.split("|")
    id_ = dat[0]
    link = dat[1]
    await add_chat(id_, link)
    await message.answer(text="Чат добавлен")
    return

@router_admin.message(F.text == 'Завершить')
async def finish_addchat_1(message: Message, state: FSMContext):
    await message.answer(text="Загрузка чатов завершена!", reply_markup=ReplyKeyboardRemove())
    await state.clear()





    



