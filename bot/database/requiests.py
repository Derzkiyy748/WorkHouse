import datetime
from datetime import datetime
from datetime import timedelta
from datetime import datetime as dt

from database.module import User, async_session, Task
from sqlalchemy import select, update
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
        

async def set_soglashenie(user_id):
    async with async_session() as session:

        await session.execute(
                                update(User)
                                .where(User.user_id == user_id)
                                .values(soglashenie="True")
                            )
        await session.commit()


async def add_task(user_id, data):
    async with async_session() as session:
        # Get current time
        time = dt.now()

        task = Task(
            user_id_task=user_id,
            worker_id_task='no',
            time=time.strftime("%Y-%m-%d|%H:%M:%S"),
            status='check',
            category=data['task_1'],
            podcategory=data['task_2'],
            min_tz=data['min_tz'],
            max_tz=data['max_tz'],
            price=data['price'],
        )

        session.add(task)
        await session.commit()

async def edit_task(user_id):
    async with async_session() as session:
        await session.execute(
                                update(Task)
                                .where(Task.user_id_task == user_id)
                                .values(status='activity')
                            )
        await session.commit()
        

async def get_task(user_id: int):
    async with async_session() as session:
        res = await session.execute(select(Task).where(Task.user_id_task == user_id).options(selectinload('*')))
        task = res.scalar()

        return task





        