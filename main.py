from aiogram.utils import executor
import logging
from config import Developers, bot, dp
import buttons
from db import ORM
from handlers import (commands, FSM_crediting_points, register_users,
                      get_all_and_delete_user, delete_user, refactor,
                      report_AntsCoins, register_admin, my_profile)


# ==================================================================================================================
async def on_startup(_):
    for Admin in Developers:
        await bot.send_message(chat_id=Admin, text="Bot started!", reply_markup=buttons.startSuperAdmin)
        await ORM.sql_create()

commands.register(dp)
FSM_crediting_points.register_user_coins(dp)
register_users.register_users(dp)

get_all_and_delete_user.register_delete(dp)
delete_user.register_user(dp)
refactor.register_edit(dp)
report_AntsCoins.register_report(dp)
register_admin.register_admin(dp)
my_profile.register_my_profile(dp)

# ===========================================================================
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
