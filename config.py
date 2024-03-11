from aiogram import Dispatcher, Bot
from decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

Admins = [995712956, ]
SuperAdmins = [995712956, ]


# ID Айданы
# Admins = [295769109, ]
# SuperAdmins = [295769109, ]

TOKEN = config('TOKEN')
bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
