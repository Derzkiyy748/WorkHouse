from aiogram.fsm.state import StatesGroup, State


class New_task(StatesGroup):
    task_1 = State()
    task_2 = State()
    min_tz = State()
    max_tz = State()
    price = State()
    chek = State()
    

