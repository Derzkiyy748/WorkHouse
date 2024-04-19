import asyncio
import time
import config

from misc.message import profile_workers
from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from keyboards.inline.worker import (main_worker, profile_worker,
                                     finish_task_worker, worker_task,
                                     activity_task_worker)

from keyboards.inline.menu import accept_user
from misc.message import open_task_user, desc_mytask_worker
from aiogram import Bot
from aiogram.types.input_file import FSInputFile
from database.requiests import (get_task, finish_task_work,
                                get_worker, get_group_work,
                                get_tasks_work, activity_task_work)

from aiogram.utils.keyboard import InlineKeyboardBuilder

from fliters.Fliter import Worker


router_worker = Router()


@router_worker.callback_query(F.data == 'worker')
async def worker(call: CallbackQuery, bot: Bot):
    await bot.edit_message_media(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        media=InputMediaPhoto(
                            media=FSInputFile(path="bot/images/kross.jpg"),
                            caption="Главное меню"
                        ),
                        reply_markup=await main_worker()
                        )
    


@router_worker.callback_query(F.data == 'profile_worker')
async def profile_worker_1(call: CallbackQuery, bot: Bot):

    work = await get_worker(call.from_user.id)
    await bot.edit_message_media(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        media=InputMediaPhoto(
                            media=FSInputFile(path="bot/images/kross.jpg"),
                            caption=profile_workers(work)
                        ),
                        reply_markup=await profile_worker(call.from_user.id)
                        )
    

@router_worker.callback_query(F.data == 'profile_back_work')
async def profile_back_work(call: CallbackQuery, bot: Bot):
    await profile_worker_1(call, bot)

@router_worker.callback_query(F.data == 'main_worker')
async def main_worker_1(call: CallbackQuery, bot: Bot):
    await bot.edit_message_media(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    media=InputMediaPhoto(
                        media=FSInputFile(path="bot/images/kross.jpg"),
                        caption="Главное меню"
                    ),
                    reply_markup=await main_worker()
                    )
    

@router_worker.callback_query(F.data.startswith("rate_"))
async def rate_worker(call: CallbackQuery, bot: Bot):
    id_ = call.data.split("_")[1]

    work = await get_worker(id_)

    await call.answer(text=f"Ваш рейтинг: {work.worker_rate}", show_alert=True)



@router_worker.callback_query(F.data.startswith("acceptwork_"))
async def accept_wok(call: CallbackQuery, bot: Bot):
    task_id, work_id  = call.data.split("_")[1], call.data.split("_")[2]
    task = await get_task(task_id)
    work = await get_worker(work_id)
    await call.message.delete()
    await call.answer(text="✔️Задание принято", show_alert=True)

    await bot.send_message(chat_id=task.user_id_task, 
                           text=open_task_user(task, work), 
                           reply_markup=await accept_user(task_id, task.user_id_task, call.from_user.id))

@router_worker.callback_query(F.data == 'main_worker_back')
async def main_worker_back(call: CallbackQuery, bot: Bot):
    await call.message.delete()
    work = await get_worker(call.from_user.id)
    await bot.send_photo(
                        chat_id=call.message.chat.id,
                        photo=FSInputFile(path="bot/images/kross.jpg"),
                        caption=profile_workers(work),       
                        reply_markup=await profile_worker(call.from_user.id)
                        )
    

@router_worker.callback_query(F.data.startswith("mytasks_"))
async def myorders_worker(call: CallbackQuery, bot: Bot):

    id_ = call.data.split("_")[1]

    await call.message.delete()

    await bot.send_photo(   
                             chat_id=call.message.chat.id,
                             photo=FSInputFile("bot/images/kross.jpg"),
                             caption=f"Выберите тип заказа: ",
                             reply_markup=await worker_task(id_)
                        )
    
@router_worker.callback_query(F.data.startswith("finishtasksworker_"))
async def finishtasks_worker(call: CallbackQuery, bot: Bot):
    id_ = call.data.split("_")[1]

    task = await finish_task_work(id_)

    await call.message.delete()

    await bot.send_photo(
                             chat_id=call.message.chat.id,
                             photo=FSInputFile("bot/images/kross.jpg"),
                             caption=f"Завершенные заказы",
                             reply_markup=await finish_task_worker(task, 0)
                        )
    
@router_worker.callback_query(F.data.startswith("activetasksworker_"))
async def activetasks_worker(call: CallbackQuery, bot: Bot):
    id_ = call.data.split("_")[1]

    task = await activity_task_work(id_)

    await call.message.delete()

    await bot.send_photo(
                             chat_id=call.message.chat.id,
                             photo=FSInputFile("bot/images/kross.jpg"),
                             caption=f"Активные заказы",
                             reply_markup=await activity_task_worker(task, 0)
                        )
    
@router_worker.callback_query(F.data == "back_prof_worker")
async def back_prof_worker(call: CallbackQuery, bot: Bot):
    await myorders_worker(call, bot)
    

@router_worker.callback_query(F.data.startswith("finmytaskworker_"))
async def mytask_worker_1(call: CallbackQuery, bot: Bot):

    id_ = call.data.split("_")[1]

    task = await get_tasks_work(call.message.chat.id)

    group = await get_group_work(id_)

    await call.message.delete()
    print(group)

    kb = InlineKeyboardBuilder()
    kb.button(text='Чат заказа', url=group.link)
    kb.button(text="<- Назад", callback_data=f"back_prof_worker")


    await bot.send_photo(   
                             chat_id=call.message.chat.id,
                             photo=FSInputFile("bot/images/kross.jpg"),
                             caption=desc_mytask_worker(task),
                             reply_markup= kb.as_markup(),
                             parse_mode='html'
                        )