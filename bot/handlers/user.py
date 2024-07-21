import asyncio
import time
from keyboards.inline.admin import new_worker_add
import config

from handlers.payment.create_link import create_link_payment, generate_order_number, check_aio_payment
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.input_file import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from keyboards.inline.menu import (admin_repl, finish_task_user, go_something, menu_keyboard, menu_profile, 
                                   menu_o_nas, menu_rules, menu_new_task_1, 
                                   menu_new_task_2, cancel_task, accept_work, 
                                   get_chat, activity_task_user, menu_ruless, payments_back, payments_vibor,
                                   user_task_, reviews_menu, create_skill_keyboard, payments)

from database.requiests import (count_finish_tasks, registration_user, get_soglashenie, set_soglashenie, 
                                get_user, add_task, activ_get_task, finish_get_task,
                                check_worker, get_chats, edit_chats, get_tasks, edits_task_,
                                get_task, get_usere, count_activ_tasks, get_reviews, paymount)

from misc.message import (
                            new_worker, open_task, new_application, desc_mytask, main_text, profile_user,
                            payment_c
                        )
from states.state import New_task, New_worker, Payment, Rew



router = Router()


new_workerrr = {
    "stack": None,
    "bio": None,
    "despt": None,
    "username": None
}


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

        if ts.status == 'активный':
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
                                photo=FSInputFile("bot/images/bot/main.jpg"),
                                caption=main_text(),
                                reply_markup=await menu_keyboard(message.chat.id, user_id_work),
                                parse_mode='html'
            )

        else:
            await message.answer(
                text="🔎Для использования бота необходимо согласиться с общими условиями",
                reply_markup=await menu_ruless()
            )


@router.callback_query(F.data == "true_rules")
async def true_rules(call: CallbackQuery, bot: Bot):
    await call.message.delete()  # Удаление сообщения от кнопки "Меню"
    await set_soglashenie(call.from_user.id)

    await bot.send_photo(
                        chat_id=call.message.chat.id,
                        photo=FSInputFile("bot/images/bot/main.jpg"),
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
                            media=FSInputFile(path="bot/images/bot/main.jpg"),
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
                                media=FSInputFile(path="bot/images/bot/main.jpg"),
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
            media=FSInputFile(path="bot/images/bot/main.jpg"),
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
            media=FSInputFile(path="bot/images/bot/main.jpg"),
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
            media=FSInputFile(path="bot/images/bot/main.jpg"),
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
                        photo=FSInputFile("bot/images/bot/main.jpg"),
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
                             photo=FSInputFile("bot/images/bot/main.jpg"),
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
                             photo=FSInputFile("bot/images/bot/main.jpg"),
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
                             photo=FSInputFile("bot/images/bot/main.jpg"),
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
                             photo=FSInputFile("bot/images/bot/main.jpg"),
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

    await call.answer("❌Данная функция в разработке", show_alert=True)


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
    
    await call.message.delete(chat_id=config.group_task,
                              message_id=task.task_id)

    await bot.send_message(chat_id=work_id,
                           text="✔️Ваше задание принято\nПерейдите в чат для дальнейших действий",
                           reply_markup=await get_chat(gr.link))
    
    await bot.send_message(chat_id=call.from_user.id,
                           text="✔️Задание принято\nПерейдите в чат для дальнейших действий",
                           reply_markup= await get_chat(gr.link))
    


@router.callback_query(F.data == "yes_rev")
async def yes_rev(call: CallbackQuery, bot: Bot, state: FSMContext):

    await call.message.delete()

    await call.message.answer(text="Поставьте, пожалуйста, оценку", reply_markup=await reviews_menu())

    await state.set_state(Rew.star)


@router.callback_query(F.data == "no_rev")
async def yes_rev(call: CallbackQuery, bot: Bot, state: FSMContext):

    await call.message.delete()

    await call.message.answer(text="Вы отказались..")

    await state.set_state(Rew.star)

    
@router.callback_query(F.data.startswith("star_"), Rew.star)
async def star(call: CallbackQuery, bot: Bot, state: FSMContext):
    star = int(call.data.split("_")[1])  # Convert to integer

    st = "⭐️" * star  # Now that star is an integer, multiplication works
    await state.update_data(star=st)

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Спасибо! Теперь напишите краткий отзыв о продавце:",
        reply_markup=None
    )

    await state.set_state(Rew.decpt)

    

@router.message(F.text, Rew.decpt)
async def decpt(msg: Message, bot: Bot, state: FSMContext):

    decpt = msg.text

    await msg.delete()

    await state.update_data(desp=decpt)
    data = await state.get_data()

    await get_reviews(data["desp"], data["star"], msg.from_user.id)

    await bot.send_message(chat_id=msg.chat.id,
                           text="Спасибо за оценку!")
    
    await state.clear()

@router.callback_query(F.data == "something")
async def something(call: CallbackQuery, bot: Bot, state: FSMContext):

    await call.message.answer(text="Вы готовы начать собеседование?", reply_markup=await go_something())


@router.callback_query(F.data == "go")
async def select_skills(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.message.delete()
    await call.message.answer('Выберите интересующие вас навыки:', reply_markup=await create_skill_keyboard([]))
    await state.set_state(New_worker.stack_1)

@router.callback_query(F.data.in_(['SQL', 'Python', 'C++', 'Java', 'JavaScript', 'HTML/CSS', 'Data Science', 'Machine Learning', 'Web Development', 'Mobile Development']),
                       New_worker.stack_1)
async def toggle_skill(call: CallbackQuery, state: FSMContext, bot: Bot):
    
    # Get the selected skills list from the state
    selected_skills = await state.get_data()
    if selected_skills is None:
        selected_skills = set()
    else:
        selected_skills = selected_skills.get('selected_skills', set())

    skill = call.data

    if skill in selected_skills:
        selected_skills.remove(skill)
    else:
        selected_skills.add(skill)

    # Update the selected skills in the state
    await state.update_data(selected_skills=selected_skills)
    new_workerrr["stack"] = selected_skills
    new_workerrr["username"] = call.from_user.username
    await state.update_data(username=call.from_user.username)

    # Update the message with the new keyboard
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        reply_markup=await create_skill_keyboard(selected_skills))
    


@router.callback_query(F.data == "continue")
async def sdadads(call: CallbackQuery, bot: Bot, state: FSMContext):

    await bot.edit_message_text(chat_id=call.message.chat.id,
                             message_id=call.message.message_id,
                             text='<b>Расскажите о себе.</b>\n\n<i>Какие проекты вы выполняли, что оказалось самым сложным, вы работали в группе или один?</i>', parse_mode='html')
    await state.set_state(New_worker.stack_2)


@router.message(F.text, New_worker.stack_2)
async def fsdf(msg: Message, bot: Bot, state: FSMContext):

    bio = msg.text

    await state.update_data(biograf=bio)
    new_workerrr["bio"] = bio

    await msg.answer(text="<b>Какие API вы знаете, где использовали?</b>", parse_mode='html')
    await state.set_state(New_worker.stack_3)



@router.message(F.text, New_worker.stack_3)
async def fsdf(msg: Message, bot: Bot, state: FSMContext):

    project = msg.text

    await state.update_data(despt=project)
    new_workerrr["despt"] = project

    data = await state.get_data()

    await bot.send_message(chat_id=config.ADMIN_ID[0],
                           text=new_worker(data),
                           reply_markup=await new_worker_add(msg.from_user.id))
    await msg.answer(text="<b>Спасибо за прохождение собеседования!</b>\n\n<i>анкета отправлена на проверку</i>", parse_mode='html')


@router.callback_query(F.data=='finish_payment')
async def fin(c: CallbackQuery, bot: Bot, state: FSMContext):
    
    state.clear()

    await bot.send_photo(
                                chat_id=c.message.chat.id,
                                photo=FSInputFile("bot/images/bot/main.jpg"),
                                caption=main_text(),
                                reply_markup=await menu_keyboard(c.message.chat.id, c.message.from_user.id),
                                parse_mode='html'
            )



@router.callback_query(F.data.startswith("replenish_"))
async def payment_1(c: CallbackQuery, bot: Bot, state: FSMContext):

    await c.message.delete()

    await c.message.answer(text="<b>Выверите способ пополнения</b>\n\n<i>пополнение через кассы от 500 рублей</i>",
                           reply_markup=await payments_vibor(),
                           parse_mode='html')
    
    await state.set_state(Payment.payment_1)

@router.callback_query(F.data == 'admin_payment', Payment.payment_1)
async def adm_pay(c: CallbackQuery, bot: Bot, state: FSMContext):

    await c.answer(text="Данная функция в разработке!", show_alert=True)

    '''
    await c.message.delete()

    await state.update_data(payment="admin_payment")

    await c.message.answer(text="<b>Введите сумму пополнения: </b>", reply_markup=await payments_back(), parse_mode='html')

    await state.set_state(Payment.payment_2)
    '''

amount = dict()

'''
@router.message(F.text, Payment.payment_2)
async def amout(m: Message, bot: Bot, state: FSMContext):

    await m.delete()

    a = m.text

    if not a.isdigit():  # Проверка, что цена является числом
        await m.answer(
            text="❌Цена должна быть числом: ",
            reply_markup=await payments_back()
        )
        return

    amount[m.chat.id] = int(a)

    await bot.send_message(chat_id=config.ADMIN_ID[0],
                           text=...)
'''  


@router.callback_query(F.data == "aio_payment", Payment.payment_1)
async def payment_2(c: CallbackQuery, bot: Bot, state: FSMContext):
    await c.message.delete()

    await state.update_data(payment="aio_payment")

    await c.message.answer(text="<b>Введите сумму пополнения: </b>", reply_markup=await payments_back(), parse_mode='html')

    await state.set_state(Payment.payment_2)

@router.message(F.text, Payment.payment_2)
async def amout(m: Message, bot: Bot, state: FSMContext):

    await m.delete()

    a = m.text

    if not a.isdigit():  # Проверка, что цена является числом
        await m.answer(
            text="❌Цена должна быть числом: ",
            reply_markup=await payments_back()
        )
        return

    await state.update_data(amount=int(a))

    data = await state.get_data()

    comment = await generate_order_number()

    date = await create_link_payment(data['amount'], comment)

    await state.update_data(form=date)

    await m.answer(text="<b>Ваша оплата готова!</b>\n\n<i>Для оплаты перейдите по кнопке:</i>",
                   reply_markup=await payments(date['url']),
                   parse_mode='html')
    
    await state.set_state(Payment.payment_3)
    

@router.callback_query(F.data == 'check_payment', Payment.payment_3)
async def ff(c: CallbackQuery, bot: Bot, state: FSMContext):

    data_form = await state.get_data()

    comment = data_form['form']

    chek = await check_aio_payment(comment)

    if chek == 200:
        await c.message.delete()
        await c.message.answer(text="<b>Спасибо за пополнение баланса в нашем проекте!</b>\n\n<i>Деньги зачислены на ваш счет</i>", parse_mode='html')
        await bot.send_message(chat_id=config.group_payment,
                               text=payment_c(data_form['payment'], comment['price']),
                               parse_mode='html')
        await paymount(comment['price'], c.message.chat.id)
        await state.clear()
        print(comment['price'], c.message.from_user.id)


    else:
        await c.message.answer(text="Вы еще не оплатили!")
 











    


