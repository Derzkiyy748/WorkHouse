from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


async def main_menu_admin():
    kb = [
        [
            InlineKeyboardButton(text="Добавить чат", callback_data="add_chat")
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