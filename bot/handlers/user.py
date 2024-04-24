import asyncio
import time
import config

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.input_file import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from keyboards.inline.menu import (admin_repl, finish_task_user, menu_keyboard, menu_profile, 
                                   menu_o_nas, menu_rules, menu_new_task_1, 
                                   menu_new_task_2, cancel_task, accept_work, 
                                   get_chat, activity_task_user,
                                   user_task_)

from database.requiests import (count_finish_tasks, registration_user, get_soglashenie, set_soglashenie, 
                                get_user, add_task, activ_get_task, finish_get_task,
                                check_worker, get_chats, edit_chats, get_tasks, edits_task_,
                                get_task, get_usere, count_activ_tasks)

from misc.message import (
                            open_task, new_application, desc_mytask, main_text, profile_user
                        )
from states.state import New_task
from handlers.admin import yes_task



router = Router()


@router.message(CommandStart())
async def start(message: Message, bot: Bot, state: FSMContext):
    dict_user = {
                'name': message.from_user.first_name,
                'username': message.from_user.username,
                'balance': 0,
                'ban': False,
                'mode': "user",
                'registration_time': time.time(),
                'reg': 1,
                'soglashenie': "False",
    }

    reg = await get_user(message.from_user.id)

    task_id = message.text[7:]
      # Получаем последнее слово из текста сообщения

    if task_id != '':
        user_id_work = message.from_user.id

        if await check_worker(user_id_work) is None:
            await message.answer(text="❌Вы не исполнитель")
            return 
        
        ts = await get_task(task_id)

        if ts.status == 'activity':
            user_id_work = message.from_user.id
            await message.answer(text=open_task(ts),
                                 reply_markup= await accept_work(task_id, user_id_work),
                                 parse_mode='html')
            
    else:

        if reg is False:
            await registration_user(message.from_user.id, dict_user)

        soglas = await get_soglashenie(message.from_user.id)

        if soglas is False:
            user_id_work = message.from_user.id
            await bot.send_photo(
                                chat_id=message.chat.id,
                                photo=FSInputFile("bot/images/main.jpg"),
                                caption=main_text(),
                                reply_markup=await menu_keyboard(message.chat.id, user_id_work),
                                parse_mode='html'
            )

        else:
            await message.answer(
                text="🔎Для использования бота необходимо согласиться с общими условиями",
                reply_markup=await menu_rules()
            )


@router.callback_query(F.data == "true_rules")
async def true_rules(call: CallbackQuery, bot: Bot):
    await call.message.delete()  # Удаление сообщения от кнопки "Меню"
    await set_soglashenie(call.from_user.id)

    await bot.send_photo(
                        chat_id=call.message.chat.id,
                        photo=FSInputFile("bot/images/kross.jpg"),
                        caption=main_text(),
                        reply_markup=await menu_keyboard(call.message.chat.id, call.from_user.id),
                        parse_mode='html'
    )


    

@router.callback_query(F.data == "profile")
async def profile(call: CallbackQuery, bot: Bot):

    if call.message.chat.id == config.ADMIN_ID[0]:
        task_1 = await count_activ_tasks(call.message.chat.id)
        task_2 = await count_finish_tasks(call.message.chat.id)
        user = await get_usere(call.message.chat.id)
        await bot.edit_message_media(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        media=InputMediaPhoto(
                            media=FSInputFile(path="bot/images/kross.jpg"),
                            caption=profile_user(user, task_1, task_2),
                            parse_mode='html'
                        ),
                        reply_markup=await menu_profile(call.message.chat.id)
                        )
    else:
                    
        await bot.edit_message_media(
                            chat_id=call.message.chat.id,
                            message_id=call.message.message_id,
                            media=InputMediaPhoto(
                                media=FSInputFile(path="bot/images/kross.jpg"),
                                caption="Профиль: "
                            ),
                            reply_markup=await menu_profile(call.message.chat.id) 
                        )
        

@router.callback_query(F.data.startswith("backprof_"))
async def back_prof(call: CallbackQuery, bot: Bot):
    await myorders(call, bot)

 
@router.callback_query(F.data == "back")
async def back(call: CallbackQuery, bot: Bot):

    await bot.edit_message_media(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(path="bot/images/main.jpg"),
            caption=main_text(),
            parse_mode='html'
        ),
        reply_markup=await menu_keyboard(call.from_user.id, call.from_user.id)
    )


@router.callback_query(F.data == "o_nas")
async def profile_11(call: CallbackQuery, bot: Bot):

    await bot.edit_message_media(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(path="bot/images/kross.jpg"),
            caption="Мы лучшие в своем деле!"
        ),
        reply_markup=await menu_o_nas()
    )

@router.callback_query(F.data == "rules")
async def rulex(call: CallbackQuery, bot: Bot):
    
    await bot.edit_message_media(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(path="bot/images/kross.jpg"),
            caption="Условия: "
        ),
        reply_markup=await menu_rules()
    )


    

@router.callback_query(F.data == "qq")
async def profile__1(call: CallbackQuery, bot: Bot):

    await call.answer(
                      text="Разработчики вас любят <3",
                      show_alert=True               
                    ) 
    
@router.callback_query(F.data == "cancel_task")
async def cancel_new_tas(call: CallbackQuery, bot: Bot, state: FSMContext):

    await call.message.delete()

    await bot.send_photo(
                        chat_id=call.message.chat.id,
                        photo=FSInputFile("bot/images/main.jpg"),
                        caption=main_text(),
                        reply_markup=await menu_keyboard(call.from_user.id, call.from_user.id),
                        parse_mode='html'
                    )
    
    await state.clear()


@router.callback_query(F.data.startswith("myordersuser_"))
async def myorders(call: CallbackQuery, bot: Bot):

    id_ = call.data.split("_")[1]

    await call.message.delete()

    await bot.send_photo(   
                             chat_id=call.message.chat.id,
                             photo=FSInputFile("bot/images/kross.jpg"),
                             caption=f"Выберите тип заказа: ",
                             reply_markup=await user_task_(id_)
                        )
    

@router.callback_query(F.data.startswith("finishtasksuser_"))
async def finishtask(call: CallbackQuery, bot: Bot):

    id_ = call.data.split("_")[1]

    task = await finish_get_task(id_)

    await call.message.delete()

    await bot.send_photo(
                             chat_id=call.message.chat.id,
                             photo=FSInputFile("bot/images/kross.jpg"),
                             caption='Завершенные задачи: ',
                             reply_markup=await finish_task_user(task, 0)
                        )
    
@router.callback_query(F.data.startswith("activetasksuser_"))
async def activetask(call: CallbackQuery, bot: Bot):

    id_ = call.data.split("_")[1]

    task = await activ_get_task(id_)

    await call.message.delete()

    await bot.send_photo(
                             chat_id=call.message.chat.id,
                             photo=FSInputFile("bot/images/kross.jpg"),
                             caption='Активные задачи: ',
                             reply_markup=await activity_task_user(task, 0)
                        )

    
@router.callback_query(F.data.startswith("next_"))
async def next_page(call: CallbackQuery, bot: Bot):
    page = int(call.data.split("_")[1])
    page += 6
    tasks = await get_tasks(call.message.chat.id)
    work = list(tasks)
    if len(work[page:]) == 0:
        await call.answer('Это последняя страница', show_alert=True)
    else:
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=activity_task_user(work, page))

@router.callback_query(F.data.startswith("prev_"))
async def prev_page(call: CallbackQuery, bot: Bot):
    page = int(call.data.split("_")[1])
    page -= 6
    tasks = await get_tasks(call.message.chat.id)
    work = list(tasks)
    if len(work[page:page-6]) == 0:
        await call.answer('Это первая страница', show_alert=True)
    else:
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=activity_task_user(work, page))

@router.callback_query(F.data.startswith("mytask_"))
async def mytask__1(call: CallbackQuery, bot: Bot):

    id_ = call.data.split("_")[1]

    task = await get_task(id_)

    user_id = task.user_id_task

    await call.message.delete()

    kb = InlineKeyboardBuilder()
    kb.button(text="<- Назад", callback_data=f"backprof_{user_id}")

    await bot.send_photo(   
                             chat_id=call.message.chat.id,
                             photo=FSInputFile("bot/images/kross.jpg"),
                             caption=desc_mytask(task),
                             reply_markup= kb.as_markup(),
                             parse_mode='html'
                        )
    
@router.callback_query(F.data == "profile_back")
async def profile_back(call: CallbackQuery, bot: Bot):
    await profile(call, bot)


@router.callback_query(F.data == "new_task")

async def new_task(
                    call: CallbackQuery,
                    bot: Bot,
                    state: FSMContext
                ):

    await call.message.delete()

    await call.message.answer(
                             text="⚙️Выберите направление: ",
                             reply_markup=await menu_new_task_1()
    )

    await state.set_state(New_task.task_1)


@router.callback_query(New_task.task_1, F.data == "it")

async def new_task_1(
                        call: CallbackQuery,
                        bot: Bot,
                        state: FSMContext
                    ):

    await call.message.delete()

    await call.message.answer(
                             text="⚙️Выберите подразделение: ",
                             reply_markup=await menu_new_task_2()
                        )
    
    await state.update_data(task_1='программирование')

    await state.set_state(New_task.task_2)


@router.callback_query(New_task.task_2, F.data == "create_0")

async def new_task_2(
                        call: CallbackQuery,
                        bot: Bot,
                        state: FSMContext
                    ):

    await call.message.delete()

    await state.update_data(task_2='написание с нуля')

    await call.message.answer(
                             text="✏️Напишите минимальное описание заказа: ",
                             reply_markup=await cancel_task()
                        )

    await state.set_state(New_task.min_tz)


@router.callback_query(F.data=="edit_script")
async def new_task_2(call: CallbackQuery, bot: Bot, state: FSMContext):

    await call.answer("❌Данная функция в разработке")


@router.message(New_task.min_tz)
async def new_task_3(msg: Message,
                     state: FSMContext,
                     bot: Bot):

    await msg.delete()

    text = msg.text

    if len(text) > 3:
        await state.update_data(min_tz=msg.text)

        await msg.answer(
                                    text="✏️Напишите максимальное описание заказа: ",
                                    reply_markup=await cancel_task()
                                )
                
        await state.set_state(New_task.max_tz)

    else:
        await msg.answer(
                                text="❌Минимальное количество букв - 3: ",
                                reply_markup=await cancel_task()
                            )
        return


@router.message(New_task.max_tz)
async def new_task_4(msg: Message,
                     bot: Bot,
                     state: FSMContext):

    text = msg.text

    if len(text) > 3:
        await state.update_data(max_tz=msg.text)

        await msg.delete()

        await msg.answer(
                                text="✏️Напишите цену заказа: ",
                                reply_markup=await cancel_task()
                            )

        await state.set_state(New_task.price)

    else:

        await msg.delete()

        await msg.answer(
                                text="❌Минимальное количество букв - 3: ",
                                reply_markup=await cancel_task()
                            )
        return


@router.message(New_task.price)
async def new_task_5(msg: Message,
                     bot: Bot,
                     state: FSMContext):

    await msg.delete()

    prices = msg.text

    if not prices.isdigit():  # Проверка, что цена является числом
        await msg.answer(
            text="❌Цена должна быть числом: ",
            reply_markup=await cancel_task()
        )
        return

    elif int(prices) > 50:
        await state.update_data(price=prices)  # Используйте prices, а не msg.text
        await state.update_data(user_id=msg.from_user.id)

        # Отправка сообщения
        sent_message = await msg.answer(
            text="✈️Заказ отправлен на модерацию!"
        )

        task_id = str(sent_message.message_id)  # Получение message_id отправленного сообщения
        await state.update_data(task_id=task_id)  # Сохранение message_id в state.data

        data = await state.get_data()
        user_id = msg.from_user.id

        await add_task(task_id, user_id, data)

        tasks = await get_task(data['task_id'])

        await bot.send_message(chat_id=config.ADMIN_ID[0],
                               text=new_application(tasks, data, user_id),
                               reply_markup=await admin_repl(task_id))

        await state.clear()

    else:
        await msg.answer(
            text="❌Минимальное количество букв - 3: ",
            reply_markup=await cancel_task()
        )
        return
    

@router.callback_query(F.data.startswith("acceptuser_"))
async def accept_user_1(call: CallbackQuery, bot: Bot):
    task_id, work_id = call.data.split("_")[1], call.data.split("_")[2]
    task = await get_task(task_id)
    await call.message.delete()
    gr = await get_chats()

    await edit_chats(work_id,
                     call.from_user.id,
                     task.task_id,
                     gr.link
                    )
    
    await edits_task_(task.task_id,
                      work_id,
                      gr.group_id)

    await bot.send_message(chat_id=work_id,
                           text="✔️Ваше задание принято\nПерейдите в чат для дальнейших действий",
                           reply_markup=await get_chat(gr.link))
    
    await bot.send_message(chat_id=call.from_user.id,
                           text="✔️Задание принято\nПерейдите в чат для дальнейших действий",
                           reply_markup= await get_chat(gr.link))
    



    








    


