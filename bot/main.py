#   ИМПОРТЫ
#----------------------------------#
import logging
import sys
import config
import asyncio
from aiogram import Bot, Dispatcher
from handlers.user import router
from handlers.admin import router_admin
from handlers.worker import router_worker
from handlers.group import router_group
from database.module import asyn_main                                                                                                            #// БРАТ, ПОДПИШИСЬ //#
#----------------------------------#
#----------------------------------#


#   СОЗДАНИЕ БОТА И ДИСПЕТЧЕРА, ИНИЦИЛИЗАЦИЯ РОУТЕРОВ, БАЗЫ ДАННЫХ
#----------------------------------#

async def main() -> None:

    
    bot = Bot(config.TOKEN)  # Создание объекта бота с использованием токена из конфига
    dp = Dispatcher()  # Создание объекта диспетчера

    await bot.send_message(chat_id=config.ADMIN_ID[0], text="Бот запущен")  # Отправка сообщения в админский чат бота

    dp.include_routers(router,
                       router_admin,
                       router_worker,
                       router_group)  # Включение роутеров в диспетчер

    await dp.start_polling(bot)  # Запуск бота с использованием long polling
#----------------------------------#
 
#   ЗАПУСК БОТА С ИСПОЛЬЗОВАНИЕМ АСИНХРОННОЙ ФУНКЦИИ
#----------------------------------#
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)  # Настройка уровня логирования
    try:
        asyncio.run(main())  # Запуск асинхронной функции main
        
    except KeyboardInterrupt:
        print("Exit")  # Обработка прерывания клавишей KeyboardInterrupt (Ctrl+C)
#----------------------------------#
#----------------------------------#

#https://t.me/+bEXRDAKOyJwwM2My -4089562965

