from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def menu_group():
    kb = [
        [
            InlineKeyboardButton(text="Данные о задании", callback_data="task_info")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard
