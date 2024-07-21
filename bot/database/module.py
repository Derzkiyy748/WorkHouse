# ИМПОРТЫ
#----------------------------------#
import config

# Импорт необходимых модулей из SQLAlchemy для работы с базой данных
from sqlalchemy import BigInteger, ForeignKey, String,  Column, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
#----------------------------------#
#----------------------------------#


#   СОЗДАНИЕ БД
#----------------------------------#
# Создание асинхронного SQLite-движка с использованием предоставленной конфигурации
engine = create_async_engine(config.SQLITEALHEMY_URL, echo=True)
# Создание асинхронного сессионного объекта для работы с движком
async_session = async_sessionmaker(engine)
# Определение базового класса для декларативного определения моделей данных
class Base(AsyncAttrs, DeclarativeBase):
    pass

# Определение модели данных для пользователя
class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    name = mapped_column(String(30))
    username: Mapped[str] = mapped_column(default=" ")
    balance: Mapped[int] = mapped_column(default=0)
    registration: Mapped[int] = mapped_column(default=0)
    ban: Mapped[int] = mapped_column(default=0)
    registration_time =  mapped_column(String)
    mode: Mapped[int] = mapped_column(default=0)
    soglashenie: Mapped[str] = mapped_column(default="False")

class Task(Base):
    __tablename__ = "task"
    task_id: Mapped[int] = mapped_column(primary_key=True)
    user_id_task = mapped_column(String(30))
    worker_id_task: Mapped[int] = mapped_column(default=0)
    time: Mapped[int] = mapped_column(default=0)
    status: Mapped[int] = mapped_column(default=0)
    category: Mapped[str] = mapped_column()
    podcategory: Mapped[str] = mapped_column()
    min_tz: Mapped[str] = mapped_column()
    max_tz: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    chat_id: Mapped[int] = mapped_column(default='no')

class Group(Base):
    __tablename__ = "group"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    link: Mapped[str] = mapped_column()
    group_id: Mapped[int] = mapped_column()
    group_user_id: Mapped[str] = mapped_column(default=" ")
    group_worker_id: Mapped[str] = mapped_column(default=" ")
    status: Mapped[str] = mapped_column(default="False")
    task_ids: Mapped[int] = mapped_column(default=0)

class Worker(Base):
    __tablename__ = "workers"
    worker_id: Mapped[int] = mapped_column(primary_key=True)
    worker_name: Mapped[str] = mapped_column()
    worker_description: Mapped[str] = mapped_column()
    worker_balance: Mapped[int] = mapped_column(default=0)
    worker_stack: Mapped[str] = mapped_column(default=" ")
    worker_status: Mapped[int] = mapped_column(default=0)
    worker_rate: Mapped[int] = mapped_column(default=0)


class Review(Base):
    __tablename__ = "reviews"
    review_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    stars: Mapped[str] = mapped_column(default=" ")
    rev_user_id: Mapped[int] = mapped_column(default=0)
    description: Mapped[str] = mapped_column(default=" ")


class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(default=" ")
    user_id: Mapped[int] = mapped_column(default=0)
    amount: Mapped[int] = mapped_column(default=0)
    cheque: Mapped[str] = mapped_column(default=" ")

 


    
    

    
async def asyn_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
#----------------------------------#
#----------------------------------#

