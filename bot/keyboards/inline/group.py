from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def menu_group():
    kb = [
        [
            InlineKeyboardButton(text="⚙️Данные о задании", callback_data="task_info")
        ],
        [
            InlineKeyboardButton(text="✏️Изменить цену", callback_data="up_price")
        ],
        [
            InlineKeyboardButton(text="🚀Завершить сделку", callback_data="finish_task")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


async def vibor_rev():
    kb = [
        [
            InlineKeyboardButton(text="✔️Оставить!", callback_data="yes_rev")
        ],
        [
            InlineKeyboardButton(text="❌Откажусь!", callback_data="no_rev")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard

