from aiogram.utils import executor
import logging
from config import SuperAdmins, bot, dp
import buttons
from db import ORM
from handlers import (commands, FSM_crediting_points, register_users, get_coins,
                      refactor_coins, get_all_and_delete_user)


# ==================================================================================================================
async def on_startup(_):
    for Admin in SuperAdmins:
        await bot.send_message(chat_id=Admin, text="Bot started!", reply_markup=buttons.startSuperAdmin)
        await ORM.sql_create()

commands.register(dp)
FSM_crediting_points.register_user_coins(dp)
register_users.register_users(dp)
get_coins.register_get(dp)

get_all_and_delete_user.register_delete(dp)
refactor_coins.register_update(dp)


# ===========================================================================
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
