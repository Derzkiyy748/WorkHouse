import config

from ctypes import Union
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from database.requiests import check_worker



#-------------------------------------------------------------#
#-------------------------------------------------------------#
        

class Worker(BaseFilter):
    async def __call__(self, update) -> bool:
        user_id = update.message.chat.id
        if await check_worker(user_id):
            return True
        return False
    
class Admin(BaseFilter):
    async def __call__(self, update) -> bool:
        user_id = update.message.chat.id
        if user_id == config.ADMIN_ID[0]:
            return True
        return False
    

 