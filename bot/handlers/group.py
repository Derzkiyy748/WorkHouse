from aiogram import Bot, Router, F, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.types import ContentType
from database.requiests import get_task, get_chatts, get_task_group, up_price, get_usere, finish_taskk, finish_taskk_2
from keyboards.inline.group import menu_group, vibor_rev
from states.state import Up_price, Rew
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.base import StorageKey
from misc.message import menu_group_text
import textwrap
import asyncio

router_group = Router()

@router_group.message(F.content_type == ContentType.NEW_CHAT_MEMBERS)
async def new_member(message: Message, bot: Bot):
    users = await bot.get_chat_member_count(message.chat.id)
    if users < 3:
        await message.reply('🤝 <b>Дождитесь другого участника.</b>\n'
                            'ℹ️ После его присоединения вам станет доступна команда /menu', parse_mode='html')
    else:
        msg = await message.reply('🤝 Второй участник присоединился!\n'
                                  'ℹ️ Вы всегда можете вызвать меню участника, написав команду /menu', parse_mode='html')
        await bot.pin_chat_message(message.chat.id, msg.message_id)


@router_group.message(F.text == "/menu", F.chat.type != "private")
async def menu_group_1(message: Message, bot: Bot):

    users = await bot.get_chat_member_count(message.chat.id)
    if users < 3:
        await message.reply('🤝 <b>Дождитесь другого участника.</b>\n'
                            'ℹ️ После его присоединения вам станет доступна команда /menu', parse_mode='html')
    else:
        await message.answer(menu_group_text(), reply_markup=await menu_group(),parse_mode='html')

    
    
@router_group.callback_query(F.data == "task_info")
async def task_info(call: CallbackQuery, bot: Bot):
    ps = await get_chatts(call.message.chat.id)
    print(call.message.chat.id)
    print(ps.task_ids)
    task = await get_task(ps.task_ids)

    await call.message.answer(
        textwrap.dedent(f'''
        Номер задания: {task.task_id}\n
        Категория: {task.category}\n
        Подкатегория: {task.podcategory}\n
        Мин.тз: {task.min_tz}\n
        Полное тз: {task.max_tz}\n\n
        Стоимость: {task.price}\n
        Дата|время создания: {task.time}'''))
    




@router_group.callback_query(F.data == 'up_price')
async def edit_price_1(call: CallbackQuery, bot: Bot):
  
   
    await call.message.answer('<b>📌Клиент и исполнитель, введите команду:</b> /edit_price <i>[ваша новая цена]</i>\n'
                              '<b>Если вы желаете её уменьшить, перед числами пишите знак</b> "-" <i>(без кавычек и [])</i>')
    

@router_group.callback_query(F.data == 'finish_task')
async def finish_task(call: CallbackQuery, bot: Bot):

    await call.message.answer('<b>📌Клиент и исполнитель,чтобы завершить сделку, введите команду</b>: /finish_task',
                              parse_mode='html')

    

edit_price = {"worker": None, "user": None}

@router_group.message(F.text.startswith("/edit_price"), F.chat.type != "private")
async def edit_price_2(msg: Message, bot: Bot, state: FSMContext):
    chat = await get_chatts(msg.chat.id)

    if len(msg.text.split(" ")) > 1:  # Check if there's a price value after splitting
        price_value = int(msg.text.split(" ")[1])
        print("Price value extracted:", price_value)  # Add this line for debugging

        print("Message sender ID:", msg.from_user.id)
        print("Group user ID:", chat.group_user_id)

        if int(msg.from_user.id) == int(chat.group_worker_id):
            edit_price["worker"] = int(price_value)
          
        elif int(msg.from_user.id) == int(chat.group_user_id):
            edit_price["user"] = int(price_value)
            print("User price updated:", price_value)  # Add this line for debugging

        else:
            msg.answer(text="❌Произошла ошибка")

        user_price = edit_price['user']
        worker_price = edit_price['worker']
        print("Edit price dict:", edit_price)  # Add this line for debugging

        if user_price is not None and worker_price is not None:
            if user_price == worker_price:
                await up_price(chat.task_ids, user_price)
                ts = await get_task(chat.task_ids)
                await msg.answer(text=f"<b>✔️Цена сделки изменена!/b>\n\n<b>К цене прибавилось:/b> +{user_price}\n\n<b>Новая цена сделки:/b> {ts.price}")
                edit_price["worker"] = None
                edit_price["user"] = None
            else:
                await msg.answer(text=f"<b>❌Цены различаются!/b>\n<b>Цена не может быть изменена/b>")
        else:
            user_price_text = '❌нет изменений' if user_price is None else user_price
            worker_price_text = '❌нет изменений' if worker_price is None else worker_price
            
            tp = await bot.send_message(
                msg.chat.id,
                text=f"<b>🚀Ждем подтверждение изменения цены сделки второго участника/b>\n\n"
                    f"<b>Цена заказчика:/b> {user_price_text}\n"
                    f"<b>Цена исполнителя:/b> {worker_price_text}"
            )
            
            await bot.pin_chat_message(msg.chat.id, message_id=tp.message_id)
    else:
        await msg.reply(text="<b>❌Необходимо указать цену после команды:/b> /edit_price [цена]")

edit_finish = {
    "worker": None,
    "user": None
}
@router_group.message(F.text == "/finish_task", F.chat.type != "private")
async def edit_price_2(msg: Message, bot: Bot, state: FSMContext):
    
    chat = await get_chatts(msg.chat.id)

    if int(msg.from_user.id) == int(chat.group_worker_id):
        edit_finish["worker"] = 1
        
    elif int(msg.from_user.id) == int(chat.group_user_id):
        edit_finish["user"] = 1
        
    else:
        await msg.answer(text="❌Произошла ошибка")
        return

    user_price = edit_finish['user']
    worker_price = edit_finish['worker']

    if user_price is not None and worker_price is not None:
        user = await get_usere(chat.group_user_id)
        ts = await get_task(chat.task_ids)

        if int(user.balance) >= int(ts.price):
            await finish_taskk(chat.task_ids)
            await finish_taskk_2(chat.group_user_id, ts.price)

            tp = await bot.send_message(
                msg.chat.id,
                text=f"<b>✔️Сделка успешно закрыта.</b>\n <i>Заказчик, с вашего баланса сняты средства за заказ.</i>",
                parse_mode='html'
            )
            await bot.pin_chat_message(msg.chat.id, message_id=tp.message_id)

            await bot.send_message(
                chat_id=chat.group_user_id,
                text=f'🚀Вы хотите оставить отзыв о работе исполнителя заказа №{ts.task_id} ?',
                reply_markup=await vibor_rev()
            )
            await state.set_state(Rew.star)

            edit_finish["worker"] = None
            edit_finish["user"] = None
        else:
            await msg.answer(
                text=f'<b>❌Покупатель {user.username}, на вашем счете недостаточно средств для оплаты.</b>\n\n<i>Пожалуйста, пополните счет и попробуйте снова</i>',
                parse_mode='html'
            )
    else:
        tp = await bot.send_message(
            msg.chat.id,
            text=f"<b>🚀Ждем подтверждение о завершение сделки второго участника</b>",
            parse_mode='html'
        )
        await bot.pin_chat_message(msg.chat.id, message_id=tp.message_id)

    







