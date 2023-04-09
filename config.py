from aiogram import Bot, Dispatcher
from  decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
TOKEN = config("TOKEN")

# ID АДМИНА
ADMIN_ID = 5673494428

bot = Bot(TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
