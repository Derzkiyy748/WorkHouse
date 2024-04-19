from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

              


async def main_worker():
    kb = [
        [
            InlineKeyboardButton(text='Профиль', callback_data='profile_worker')
        ],
        [
            InlineKeyboardButton(text="<- Назад", callback_data="back")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard

async def profile_worker(worker_id):
    kb = [
        [
            InlineKeyboardButton(text='Мой рейтинг', callback_data=f'rate_{worker_id}'),
            InlineKeyboardButton(text='Мои заказы', callback_data=f'mytasks_{worker_id}')
        ],
        [
            InlineKeyboardButton(text='настройки', callback_data='setting_worker')
        ],
        [
            InlineKeyboardButton(text='<- Назад', callback_data='main_worker')
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard

async def worker_task(worker_id):
    kb = [
        [
            InlineKeyboardButton(text='Завершенные', callback_data=f'finishtasksworker_{worker_id}'),
            InlineKeyboardButton(text='Активные', callback_data=f'activetasksworker_{worker_id}')
        ],
        [
            InlineKeyboardButton(text='<- Назад', callback_data='main_worker')
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


async def finish_task_worker(data, page: int):
    kb = InlineKeyboardBuilder()
    data_list = list(data)
    if data == []:
        kb.row(InlineKeyboardButton(text='Заказов нет', callback_data='sklfjsda'))
        kb.row(InlineKeyboardButton(text='<- Назад', callback_data='profile_back'))
        return kb.as_markup()
    
    start_index = page * 6
    end_index = min(start_index + 6, len(data_list))  # Ensure we don't exceed the length of the data
    
    for i in data_list[start_index:end_index]:
        kb.add(InlineKeyboardButton(text=f'📚 {i.task_id} | {i.category}', callback_data=f'finmytaskworker_{i.task_id}'))
    
    # Add navigation buttons and page number
    kb.row(
        InlineKeyboardButton(text='<-', callback_data=f'prev_{page}'),
        InlineKeyboardButton(text=f'{page + 1}/{(len(data_list) + 5) // 6}', callback_data='sklfjsda'),  # Assuming 6 tasks per page
        InlineKeyboardButton(text='->', callback_data=f'next_{page}')
    )
    kb.row(
        InlineKeyboardButton(text='<- Назад', callback_data='profile_back_work')
    )

    return kb.as_markup()


async def activity_task_worker(data, page: int):
    kb = InlineKeyboardBuilder()
    data_list = list(data)
    if data == []:
        kb.row(InlineKeyboardButton(text='Заказов нет', callback_data='sklfjsda'))
        kb.row(InlineKeyboardButton(text='<- Назад', callback_data='profile_back'))
        return kb.as_markup()
    
    start_index = page * 6
    end_index = min(start_index + 6, len(data_list))  # Ensure we don't exceed the length of the data
    
    for i in data_list[start_index:end_index]:
        kb.add(InlineKeyboardButton(text=f'📚 {i.task_id} | {i.category}', callback_data=f'finmytaskworker_{i.task_id}'))
    
    # Add navigation buttons and page number
    kb.row(
        InlineKeyboardButton(text='<-', callback_data=f'prev_{page}'),
        InlineKeyboardButton(text=f'{page + 1}/{(len(data_list) + 5) // 6}', callback_data='sklfjsda'),  # Assuming 6 tasks per page
        InlineKeyboardButton(text='->', callback_data=f'next_{page}')
    )
    kb.row(
        InlineKeyboardButton(text='<- Назад', callback_data='profile_back_work')
    )
    return kb.as_markup()

