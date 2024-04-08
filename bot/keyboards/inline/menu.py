from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



async def menu_keyboard():
    kb = [
        [
            InlineKeyboardButton(text="💎Сделать заказ", callback_data="new_task")
        ],
        [
            InlineKeyboardButton(text="💎О нас", callback_data="o_nas"),
            InlineKeyboardButton(text="💎Правила", callback_data="rules")
        ],
        [
            InlineKeyboardButton(text="💎Профиль", callback_data="profile")
        ],
        [
            InlineKeyboardButton(text="🏘️Устроиться🏘️", callback_data="something")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


async def menu_profile():
    kb = [
        [
            InlineKeyboardButton(text="📩Мои заказы", callback_data="my_orders"),
        
            InlineKeyboardButton(text="📩Мои чаты", callback_data="my_chats")
        ],
        [
            InlineKeyboardButton(text="<- Назад", callback_data="back")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


async def menu_o_nas():
    kb = [[
            InlineKeyboardButton(text="Разработчик", callback_data="qq")
        ],
        [
            InlineKeyboardButton(text="@D3rzkiyy", url="http://t.me/D3rzkiyy")
        ],
        [
            InlineKeyboardButton(text="<- Назад", callback_data="back")
        ]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


async def menu_rules():
    kb = [
        [
            InlineKeyboardButton(text="✔️Согласиться", callback_data="true_rules")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


async def menu_new_task_1():
    kb = [
        [
            InlineKeyboardButton(text="Программирование", callback_data="it")
        ],
        [
            InlineKeyboardButton(text="❌Отмена", callback_data="cancel_task")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


async def menu_new_task_2():
    kb = [
        [
            InlineKeyboardButton(text="Написание с нуля", callback_data="create_0")
        ],
        [
            InlineKeyboardButton(text="Исправление багов", callback_data="edit_script")
        ],
        [
            InlineKeyboardButton(text="❌Отмена", callback_data="cancel_task")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


async def cancel_task():
    kb = [
        
        [
            InlineKeyboardButton(text="❌Отмена", callback_data="cancel_task")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


async def admin_repl():
    kb = [

        [
            InlineKeyboardButton(text="Принять", callback_data="yes_task"),
            InlineKeyboardButton(text="Отклонить", callback_data="no_task")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard

async def play():
    kb = [
        [
            InlineKeyboardButton(text="Жми", web_app=...)
        ]
    ]



