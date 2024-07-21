from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


async def main_menu_admin():
    kb = [
        [
            InlineKeyboardButton(text="Добавить чат", callback_data="add_chat")
        ], 
        [
            InlineKeyboardButton(text="<- Назад", callback_data="back")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


async def finish_addchat():
    kb = [
        [
            KeyboardButton(text="Завершить")
        ],
        [
            KeyboardButton(text="Отмена")
        ]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


async def new_worker_add(worker_id: int):
    kb = [
        [
            InlineKeyboardButton(text="Принять", callback_data=f"addwork_{worker_id}")
        ],
        [
            InlineKeyboardButton(text="Отклонить", callback_data=f"nowork_{worker_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)