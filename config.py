from aiogram import Dispatcher, Bot
from decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# TOKEN = "6570711981:AAGo0p436G80I_ziI24xTQblz3Z-LhPnM5w"
# Admins = [995712956, ]
# SuperAdmins = [995712956, ]

# =======================================================================
# Рабочие!
Admins = [793829796, 6312117749, 348257044, 5854709440]
SuperAdmins = [995712956, 295769109, 995712956, 910527902, 448059036, 985526419, ]
# =======================================================================

Developers = [995712956, ]
TOKEN = config('TOKEN')
bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
