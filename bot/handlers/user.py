import asyncio
import time
import config

from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from keyboards.inline.menu import admin_repl, menu_keyboard, menu_profile, menu_o_nas, menu_rules, menu_new_task_1, menu_new_task_2, cancel_task
from aiogram import Bot
from aiogram.types.input_file import FSInputFile
from database.requiests import registration_user, get_soglashenie, set_soglashenie, get_user, add_task, get_task
from states.state import New_task
from handlers.admin import yes_task





router = Router()

@router.message(CommandStart())
async def start(message: Message, bot: Bot):
    dict_user = {
                'name': message.from_user.first_name,
                'balance': 0,
                'ban': False,
                'mode': "user",
                'registration_time': time.time(),
                'reg': 1,
                'soglashenie': "False",
    }

    reg = await get_user(message.from_user.id)

    if reg is False:
        await registration_user(message.from_user.id, dict_user)

    soglas = await get_soglashenie(message.from_user.id)

    if soglas is False:
        await bot.send_photo(
                            chat_id=message.chat.id,
                            photo=FSInputFile("bot/images/kross.jpg"),
                            caption="Меню: ",
                            reply_markup=await menu_keyboard()
        )
    else:
        await message.answer(
            text="Для использования бота необходимо согласиться с общими условиями",
            reply_markup=await menu_rules()
        )


@router.callback_query(F.data == "true_rules")
async def true_rules(call: CallbackQuery, bot: Bot):
    await call.message.delete()  # Удаление сообщения от кнопки "Меню"
    await set_soglashenie(call.from_user.id)

    await bot.send_photo(
                        chat_id=call.message.chat.id,
                        photo=FSInputFile("bot/images/kross.jpg"),
                        caption="Меню: ",
                        reply_markup=await menu_keyboard()
    )

    
    

@router.callback_query(F.data == "profile")
async def profile(call: CallbackQuery, bot: Bot):

    await bot.edit_message_media(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        media=InputMediaPhoto(
                            media=FSInputFile(path="bot/images/kross.jpg"),
                            caption="Профиль: "
                        ),
                        reply_markup=await menu_profile() 
                    )
    

 
@router.callback_query(F.data == "back")
async def back(call: CallbackQuery, bot: Bot):

    await bot.edit_message_media(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        media=InputMediaPhoto(
            media=FSInputFile(path="bot/images/kross.jpg"),
            caption="Меню: "
        ),
        reply_markup=await menu_keyboard()
    )


@router.callback_query(F.data == "o_nas")
async def profile(call: CallbackQuery, bot: Bot):

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
async def profile(call: CallbackQuery, bot: Bot):

    await call.answer(
                      text="Разработчики вас любят <3",
                      show_alert=True               
                    ) 
    
@router.callback_query(F.data == "cancel_task")
async def cancel_new_tas(call: CallbackQuery, bot: Bot, state: FSMContext):

    await call.message.delete()

    await bot.send_photo(
                        chat_id=call.message.chat.id,
                        photo=FSInputFile("bot/images/kross.jpg"),
                        caption="Меню: ",
                        reply_markup=await menu_keyboard() 
                    )
    
    await state.clear()

    
    

@router.callback_query(F.data == "new_task")

async def new_task(
                    call: CallbackQuery,
                    bot: Bot,
                    state: FSMContext
                ):

    await call.message.delete()

    await call.message.answer(
                             text="Выберите направление: ",
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
                             text="Выберите подразделение: ",
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
                             text="Напиши минимальное описание заказа: ",
                             reply_markup=await cancel_task()
                        )

    await state.set_state(New_task.min_tz)


@router.callback_query(F.data=="edit_script")
async def new_task_2(call: CallbackQuery, bot: Bot, state: FSMContext):

    await call.answer("Данная функция в разработке")


@router.message(New_task.min_tz)
async def new_task_3(msg: Message,
                     state: FSMContext,
                     bot: Bot):

    await msg.delete()

    text = msg.text

    if len(text) > 3:
        await state.update_data(min_tz=msg.text)

        await msg.answer(
                                    text="Напиши максимальное описание заказа: ",
                                    reply_markup=await cancel_task()
                                )
                
        await state.set_state(New_task.max_tz)

    else:
        await msg.answer(
                                text="Минимальное количество букв - 3: ",
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
                                text="Напиши цену заказа: ",
                                reply_markup=await cancel_task()
                            )

        await state.set_state(New_task.price)

    else:

        await msg.delete()

        await msg.answer(
                                text="Минимальное количество букв - 3: ",
                                reply_markup=await cancel_task()
                            )
        return


@router.message(New_task.price)
async def new_task_5(msg: Message,
                     bot: Bot,
                     state: FSMContext):

    await msg.delete()

    prices = msg.text

    if int(prices) > 50:
        await state.update_data(price=msg.text)
        await state.update_data(user_id=msg.from_user.id)

        data = await state.get_data()
        user_id = msg.from_user.id

        await add_task(user_id, data)

        tasks = await get_task(user_id)


        texts = f'''
        Новая заявка!\n\n
        задание № {tasks.task_id}\n
        заказчик: {user_id}\n\n
        категория: {data["task_1"]}\n
        подразделение: {data["task_2"]}\n
        минимальное описание: {data["min_tz"]}\n
        максимальное описание: {data["max_tz"]}\n\n
        цена: {data["price"]}
        '''

        await msg.answer(
                                text="Заказ отправлен на модерацию!"
                            )
        
        await bot.send_message(chat_id=config.ADMIN_ID[0], text=texts, reply_markup=await admin_repl())

        await state.set_state(New_task.chek)

    else:
        await msg.answer(
                                text="Минимальное количество букв - 3: ",
                                reply_markup=await cancel_task()
                            )
        return  
    








    


