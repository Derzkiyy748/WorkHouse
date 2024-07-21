import datetime
from datetime import datetime
from datetime import timedelta
from datetime import datetime as dt
from sqlalchemy.sql import text

from database.module import User, async_session, Task, Worker, Group, Review
from sqlalchemy import func, select, update, delete, insert, table, column
from sqlalchemy.orm import selectinload

from typing import Tuple, Union



async def get_user(user_id: int) -> Union[User, None]:
    async with async_session() as session:
        res = await session.execute(select(User).where(User.user_id == user_id))
        r = res.scalar()
        if r:
            return True
        else:
            return False
        
async def get_usere(user_id: int):
    async with async_session() as session:
        res = await session.execute(select(User)
                                    .where(User.user_id == user_id)
                                    .options(selectinload('*')))
        r = res.scalar()
        return r


async def registration_user(
                            user_id: int,
                            dict_user: dict,
                        ) -> Union[User, None]:
    
    async with async_session() as session:
        async with session.begin():

            res = await session.execute(select(User).where(User.user_id == user_id))

            if res.scalars():

                time = dt.now()

                user = User(
                    user_id=user_id,
                    name=dict_user['name'],
                    username=dict_user['username'],
                    balance=dict_user['balance'],
                    registration=dict_user['reg'],
                    ban=dict_user['ban'],
                    mode=dict_user['mode'],
                    registration_time=time.strftime("%Y-%m-%d|%H:%M:%S"),
                    soglashenie=dict_user['soglashenie'],
                )

                session.add(user)
                await session.commit()

            else:
                return False


async def finish_taskk(task_id: int):
    async with async_session() as session:
        await session.execute(
                            update(Task)
                            .where(Task.task_id == task_id)
                            .values(status="завершенный")
                        )
        await session.commit()

async def finish_taskk_2(user_id: int, money: int):
     async with async_session() as session:
        await session.execute(
                            update(User)
                            .where(User.user_id == user_id)
                            .values(balance=User.balance - money)
                        )
        await session.commit()

async def set_star(user_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(Review)
            .where(Review.rev_user_id == user_id)
            .options(selectinload('*'))
        )
        reviews = result.scalars().all()
        return reviews
    

async def get_reviews(descp, star, user_id):
    async with async_session() as session:

        await session.execute(
                    insert(Review)
                    .values(description=descp,
                            rev_user_id=user_id,
                            stars=star)
        )
        await session.commit()


async def get_soglashenie(
                          user_id: int
                        ) -> Union[str, None]:

    async with async_session() as session:
        res = await session.execute(
                                    select(User.soglashenie)
                                    .where(User.user_id == user_id)
                                )
        r = res.scalar()

        if r == "True":
            return False
        else:
            return True
        

async def set_soglashenie(user_id: int) -> None:
    async with async_session() as session:

        await session.execute(
                                update(User)
                                .where(User.user_id == user_id)
                                .values(soglashenie="True")
                            )
        await session.commit()


async def add_task(post_id: int, user_id: int, data: dict):
    async with async_session() as session:
        # Get current time
        time = dt.now()

        task = Task(
            task_id = post_id,
            user_id_task=user_id,
            worker_id_task='no',
            time=time.strftime("%Y-%m-%d|%H:%M:%S"),
            status='проверка',
            category=data['task_1'],
            podcategory=data['task_2'],
            min_tz=data['min_tz'],
            max_tz=data['max_tz'],
            price=data['price'],
        )

        session.add(task)
        await session.commit()

async def full_add_task(task_id: int):
    async with async_session() as session:
        await session.execute(
                                update(Task)
                                .where(Task.task_id == task_id)
                                .values(status='активный')
                            )
        await session.commit()

async def edits_task_(task_id: int, worker_ids: int, chat_ids):
    async with async_session() as session:
        await session.execute(
                                update(Task)
                                .where(Task.task_id == task_id)
                                .values(
                                    worker_id_task=worker_ids,
                                    chat_id=chat_ids
                                )
                            )
        await session.commit()


async def delete_task(task_id: int) -> None:
    async with async_session() as session:
        await session.execute(
                                delete(Task)
                                .where(Task.task_id == task_id)
                                
                            )
        await session.commit()
        

async def get_task(task_id: int):
    async with async_session() as session:
        res = await session.execute(
                                    select(Task)
                                    .where(Task.task_id == task_id,)
                                    .options(selectinload('*')))
        task = res.scalar()

        return task
    
async def get_task_group(chat_id: int):
    async with async_session() as session:
        res = await session.execute(
                                    select(Task)
                                    .where(Task.chat_id == chat_id,)
                                    .options(selectinload('*')))
        task = res.scalar()

        return task
    
async def up_price(task_id: int, prices: int):
    async with async_session() as session:
        await session.execute(
                                update(Task)
                                .where(Task.task_id == task_id)
                                .values(price=Task.price + prices)
                            )
        await session.commit()
    
async def get_tasks(user_id: int):
    async with async_session() as session:
        res = await session.execute(
            select(Task).where(Task.user_id_task == user_id)
        )
        tasks = res.scalars().all()
        return tasks

async def activ_get_task(user_id: int):
    async with async_session() as session:
        res = await session.scalars(
                                    select(func.count())
                                    .where(Task.user_id_task == user_id,
                                           Task.status=='активный')
                                        )

        return res
    
async def count_activ_tasks(user_id: int):
    async with async_session() as session:

        count = await session.execute(
                                select(Task.task_id)
                                .where(Task.user_id_task == user_id, Task.status == 'активный')
                            )
    ts = count.scalars().all()
    return len([item for item in ts])

async def count_finish_tasks(user_id: int):
    async with async_session() as session:

        count = await session.execute(
                                      select(Task.task_id)
                                      .where(Task.user_id_task == user_id,
                                             Task.status == 'завершенный'))

    ts = count.scalars().all()
    return len([item for item in ts])
    


async def count_activ_tasks_work(worker_id: int):
    async with async_session() as session:

        count = await session.execute(select(Task).where(Task.worker_id_task == worker_id,
                                                 Task.status == 'активный'))

    ts = count.scalars().all()
    return len([item for item in ts])

async def count_finish_tasks_work(worker_id: int):
    async with async_session() as session:

        count = await session.execute(select(Task).where(Task.worker_id_task == worker_id,
                                                 Task.status == 'завершенный'))
    ts = count.scalars().all()
    return len([item for item in ts])


    
async def finish_get_task(user_id: int):
    async with async_session() as session:
        res = await session.scalars(
                                    select(Task)
                                    .where(Task.user_id_task == user_id,
                                           Task.status=='завершенный')
                                    )
        return res

async def get_worker(worker_id: int):
    async with async_session() as session:
        res = await session.execute(
                                    select(Worker)
                                    .where(Worker.worker_id == worker_id)
                                    .options(selectinload('*')))
        worker = res.scalar()

        return worker
    
async def check_worker(worker_id: int) -> bool:
    async with async_session() as session:
        res = await session.execute(
            select(Worker)
            .where(Worker.worker_id == worker_id)
        )
        return res.scalar()

    
async def add_chat(id_: int, link: str) -> None:
    async with async_session() as session:
        await session.execute(
                    insert(Group)
                    .values(group_id=id_, link=link)
        )

        await session.commit()



async def get_chats() -> Group:
    async with async_session() as session:
        result = await session.execute(
            select(Group)
            .where(Group.status == 'False')  # Используем строку 'False' для сравнения
            .order_by(func.random())
            .limit(1)
        )
        chat = result.scalar_one_or_none()
        return chat
    

async def get_chatts(id: int):
    async with async_session() as session:
        res = await session.execute(
                select(Group)
                .where(Group.group_id == id)
                )
        
        ch = res.scalar()
            
        return ch
    
async def finish_task_work(id_: int):
    async with async_session() as session:
        res = await session.scalars(
                select(Task)
                .where(Task.worker_id_task == id_,
                       Task.status == 'завершенный')
                )

        return res
    
async def activity_task_work(id_: int):
    async with async_session() as session:
        res = await session.scalars(
                select(Task)
                .where(Task.worker_id_task == id_,
                       Task.status == 'активный')
                )

        return res
    
async def get_tasks_work(task_id: int):
    async with async_session() as session:
        res = await session.execute(
                                    select(Task)
                                    .where(Task.worker_id_task == task_id)
                                    .options(selectinload('*')))
        task = res.scalar()

        return task
    
async def get_group_work(id_: int):
    async with async_session() as session:
        res = await session.execute(
                                    select(Group)
                                    .where(Group.task_ids == id_)
                                    )
        gr = res.scalar()
        return gr

    

async def edit_chats(worker_id, user_id, task_id, link):
    """
    param: worker_id: айди воркера
    param: user_id: айди юзера
    param: task_id: айди задания
    param: link: ссылка на чат
    return: Обновляет чат на статус 'True'
    """
    async with async_session() as session:
        await session.execute(
                                update(Group)
                                .where(Group.link== link)
                                .values(status='True',
                                        group_worker_id=worker_id,
                                        group_user_id=user_id,
                                        task_ids=task_id,
                                        )
                            )
        await session.commit()



async def add_worker(worker_id: int,
                     username: str,
                     descriptionn: str,
                     balance: int,
                     stack: str):
    async with async_session() as session:
        await session.execute(
                    insert(Worker)
                    .values(worker_id=worker_id,
                            worker_description=descriptionn,
                            worker_name=username,
                            worker_balance=balance,
                            worker_stack=stack,
                            worker_rate=0,
                            worker_status=" ")
        )

        await session.commit()


async def paymount(amount, user_id):
    """
    param: amount: сумма пополнения
    return: Обновляет баланс пользователя
    """
    async with async_session() as session:
        await session.execute(
            update(User)
            .where(User.user_id == user_id)
            .values(balance=User.balance + amount)
        )
        await session.commit()



        