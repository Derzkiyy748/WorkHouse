from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import ContentType
from database.requiests import get_task, get_chatts
from keyboards.inline.group import menu_group
import textwrap

router_group = Router()

@router_group.message(F.content_type == ContentType.NEW_CHAT_MEMBERS)

async def new_member(message: Message, bot: Bot):
    users = await bot.get_chat_member_count(message.chat.id)
    if users <= 4:
        await message.reply('🤝 <b>Дождитесь другого участника.</b>\n'
                            'ℹ️ После его присоединения вам станет доступна команда /menu')
    else:
        msg = await message.reply('🤝 Второй участник присоединился!\n'
                                  'ℹ️ Вы всегда можете вызвать меню участника, написав команду /menu')
        await bot.pin_chat_message(message.chat.id, msg.message_id)


@router_group.message(F.text == "/menu", F.chat.type != "private")
async def menu_group_1(message: Message, bot: Bot):
    await message.answer('📋 Меню', reply_markup=await menu_group())

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