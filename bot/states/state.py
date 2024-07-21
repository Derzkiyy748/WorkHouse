

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

class Payment(StatesGroup):
    payment_1 = State()
    payment_2 = State()
    payment_3 = State()
    admin_payment = State()
    


'''# Шифр букв
import random


def find_smallest_number():
    number = 100
    while number % 2 != 0:
        number += 1
    return number

result = find_smallest_number()
print(result)


for x in range(100, 0, -1):
    if x < 7 and not(x < 6):
        print(x)
        break


def f(x, i):
    x = int(str(x), i)
    return x
print(min(f(47, 16), f(73, 8), f(101110, 2)))


for b in range(1, 100):
    x = 1 * b + 2 + 2 + 2
    if (x * b) == 91:
        print(b)
'''
