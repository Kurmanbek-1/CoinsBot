from aiogram.utils import executor
import logging
from config import Admins, bot, dp
import buttons
from handlers import (commands, FSM_crediting_points, register_users, get_coins,
                      refactor_coins, get_all_and_delete_user)
from db import ORM


# ==================================================================================================================
async def on_startup(_):
    for Admin in Admins:
        await bot.send_message(chat_id=Admin, text="Бот запущен!", reply_markup=buttons.startSuperAdmin)
        await ORM.sql_create()

commands.register(dp)
FSM_crediting_points.register_user_coins(dp)
register_users.register_users(dp)
get_coins.register_get(dp)

get_all_and_delete_user.register_delete(dp)
refactor_coins.register_update(dp)

# @dp.message_handler()
# async def echo(message: types.Message):
#     await message.answer('Такой команды нет ❌\n'
#                          'Нажмите на /start и у вас выйдут все ваши кнопки!')


# ===========================================================================
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
