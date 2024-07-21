from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.requiests import check_worker, get_tasks
import config



async def menu_keyboard(message_id: int, worker_id: int):
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
        ]
    ]
    is_worker = await check_worker(worker_id)
    if not is_worker:
        kb.append([
            InlineKeyboardButton(text="🏘️Устроиться🏘️", callback_data="something")
        ])
    else:
        kb.append([
            InlineKeyboardButton(text="💎Рабочий", callback_data="worker")
        ])
    if message_id == config.ADMIN_ID[0]:
        kb.append([
            InlineKeyboardButton(text="💎Админ-панель", callback_data="admin")
        ])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard

async def go_something():
    kb = [
        [
            InlineKeyboardButton(text='Даа', callback_data="go")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard

async def menu_profile(user_id: int):
    kb = [
        [
            InlineKeyboardButton(text="📩Мои заказы", callback_data=f"myordersuser_{user_id}"),
            InlineKeyboardButton(text="Пополнить", callback_data=f"replenish_{user_id}")
        ],
        [
            InlineKeyboardButton(text="<- Назад", callback_data="back")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


async def user_task_(user_id: int):
    kb = [
        [
            InlineKeyboardButton(text='Завершенные', callback_data=f'finishtasksuser_{user_id}'),
            InlineKeyboardButton(text='Активные', callback_data=f'activetasksuser_{user_id}')
        ],
        [
            InlineKeyboardButton(text='<- Назад', callback_data='profile')
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


async def finish_task_user(data, page: int):
    kb = InlineKeyboardBuilder()
    data_list = list(data)
    if data_list == [] or None:
        kb.row(InlineKeyboardButton(text='Заказов нет', callback_data='sklfjsda'))
        kb.row(InlineKeyboardButton(text='<- Назад', callback_data='profile_back'))
        return kb.as_markup()
    
    
    start_index = page * 6
    end_index = min(start_index + 6, len(data_list))  # Ensure we don't exceed the length of the data
    
    for i in data_list[start_index:end_index]:
        kb.add(InlineKeyboardButton(text=f'📚 {i.task_id} | {i.category}', callback_data=f'mytask_{i.task_id}'))
    
    # Add navigation buttons and page number
    kb.row(
        InlineKeyboardButton(text='<-', callback_data=f'prev_{page}'),
        InlineKeyboardButton(text=f'{page + 1}/{(len(data_list) + 5) // 6}', callback_data='sklfjsda'),  # Assuming 6 tasks per page
        InlineKeyboardButton(text='->', callback_data=f'next_{page}')
    )
    kb.row(
        InlineKeyboardButton(text='<- Назад', callback_data='profile_back')
    )
    print(data_list)
    print(data)
    return kb.as_markup()


async def activity_task_user(data, page: int):
    kb = InlineKeyboardBuilder()
    data_list = list(data)
    if data_list == [] or None:
        kb.row(InlineKeyboardButton(text='Заказов нет', callback_data='sklfjsda'))
        kb.row(InlineKeyboardButton(text='<- Назад', callback_data='profile_back'))
        return kb.as_markup()
    
    
    start_index = page * 6
    end_index = min(start_index + 6, len(data_list))  # Ensure we don't exceed the length of the data
    
    for i in data_list[start_index:end_index]:
        kb.add(InlineKeyboardButton(text=f'📚 {i.task_id} | {i.category}', callback_data=f'mytask_{i.task_id}'))
    
    # Add navigation buttons and page number
    kb.row(
        InlineKeyboardButton(text='<-', callback_data=f'prev_{page}'),
        InlineKeyboardButton(text=f'{page + 1}/{(len(data_list) + 5) // 6}', callback_data='sklfjsda'),  # Assuming 6 tasks per page
        InlineKeyboardButton(text='->', callback_data=f'next_{page}')
    )
    kb.row(
        InlineKeyboardButton(text='<- Назад', callback_data='profile_back')
    )
    print(data_list)
    print(data)
    return kb.as_markup()




async def menu_o_nas():
    kb = [[
            InlineKeyboardButton(text="Разработчик+поддержка", url="http://t.me/D3rzkiyy")
        ],
        [
            InlineKeyboardButton(text="<- Назад", callback_data="back")
        ]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


async def menu_rules():
    kb = [
        [
            InlineKeyboardButton(text="Тык", url=config.RULES)
        ],
        [
            InlineKeyboardButton(text="<- Назад", callback_data="back")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard

async def menu_ruless():
    kb = [
        [
            InlineKeyboardButton(text="Тык", url=config.RULESS)
        ],
        [
            InlineKeyboardButton(text="Принять", callback_data="true_rules")
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


async def admin_repl(task_id):
    kb = [

        [
            InlineKeyboardButton(text="Принять", callback_data=f"yestask_{task_id}"),
            InlineKeyboardButton(text="Отклонить", callback_data=f"notask_{task_id}")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard



async def accept(task_id):
    kb = [
        [
            InlineKeyboardButton(text="Взять задание", url=f'https://t.me/WorkHouseBot_bot?start={str(task_id)}')
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


async def accept_work(task_id, work_id):
    kb = [
        [
            InlineKeyboardButton(text="Подтвердить", callback_data=f'acceptwork_{task_id}_{work_id}'),
            InlineKeyboardButton(text="отменить", callback_data="cancel_task")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


async def accept_user(task_id, user_id, work_id):
    kb = [
        [
            InlineKeyboardButton(text="Подтвердить", callback_data=f'acceptuser_{task_id}_{work_id}'),
            InlineKeyboardButton(text="отменить", callback_data="cancel_task")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard



async def get_chat(chat_link):
    kb = [
        [
            InlineKeyboardButton(text="Зайдите в чат", url = f'{chat_link}')
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard



async def neworker_stack_1():
    kb = [
        [
            InlineKeyboardButton(text="Программирование", callback_data="programmist")
        ],
        [
            InlineKeyboardButton(text="Дизайнер", callback_data="designer")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard

async def neworker_stack_2():
    ...



async def reviews_menu():
    kb = [
        [
            InlineKeyboardButton(text="⭐️", callback_data="star_1")
        ],
        [
            InlineKeyboardButton(text="⭐️⭐️", callback_data="star_2")
        ],
        [
            InlineKeyboardButton(text="⭐️⭐️⭐️", callback_data="star_3")
        ],
        [
            InlineKeyboardButton(text="⭐️⭐️⭐️⭐️", callback_data="star_4")
        ],
        [
            InlineKeyboardButton(text="⭐️⭐️⭐️⭐️⭐️", callback_data="star_5")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


async def create_skill_keyboard(selected_skills):
    skills = ['SQL', 'Python', 'C++', 'Java', 'JavaScript', 'HTML/CSS', 'SQLalchemy', 'MySQL', 'PostgreSQL']

    kb = InlineKeyboardBuilder()
    
    for skill in skills:
        button_text = f'✅{skill}' if skill in selected_skills else skill
        kb.add(InlineKeyboardButton(text=button_text, callback_data=skill))
    
    kb.row(
        InlineKeyboardButton(text='Отмена', callback_data='back'),
        InlineKeyboardButton(text='Продолжить ->', callback_data='continue')
    )
    return kb.adjust(2).as_markup()



async def payments_vibor():
    kb = [
        [
            InlineKeyboardButton(text="AioKassa", callback_data='aio_payment')
        ],
        [
            InlineKeyboardButton(text="Админ-оплата", callback_data='admin_payment')
        ],
        [
            InlineKeyboardButton(text="Отмена", callback_data='finish_payment')
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


async def payments_back():
    kb = [
        [
            InlineKeyboardButton(text="Отмена", callback_data='finish_payment')
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


async def payments(payment_link):
    kb = [
        [
            InlineKeyboardButton(text="Оплатить", url=payment_link)
        ],
        [
            InlineKeyboardButton(text="Проверить", callback_data="check_payment")
        ],
        [
            InlineKeyboardButton(text="Отмена", callback_data='finish_payment')
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)