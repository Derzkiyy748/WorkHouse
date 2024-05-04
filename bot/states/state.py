from aiogram.fsm.state import StatesGroup, State


class New_task(StatesGroup):
    task_1 = State()
    task_2 = State()
    min_tz = State()
    max_tz = State()
    price = State()

class AddChats(StatesGroup):
    add_chats = State()
    finish = State()

class Up_price(StatesGroup):
    up_price_1 = State()
    up_price_2 = State()

class New_worker(StatesGroup):
    stack_1 = State()
    stack_2 = State()
    stack_3 = State()

class Rew(StatesGroup):
    star = State()
    decpt = State()
    

