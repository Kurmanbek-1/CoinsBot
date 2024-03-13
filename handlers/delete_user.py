from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.ORM import cursor, db
from config import bot, SuperAdmins


async def sql_command_delete(user_id):
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()


async def delete_staff_by_city(message: types.Message):
    if message.from_user.id in SuperAdmins:
        employees = cursor.execute("SELECT * FROM users").fetchall()
        if not employees:
            await message.answer("Список пуст!")

        else:
            for user in employees:
                await message.answer(text=f"Name - {user[1]}\n"
                                          f"Telegram ID - {user[2]}",
                                     reply_markup=InlineKeyboardMarkup().add(
                                         InlineKeyboardButton(f"Удалить",
                                                              callback_data=f"delete_user {user[0]}")))

    else:
        await message.answer("У вас нет прав к этой команде!")


async def complete_delete_staff(call: types.CallbackQuery):
    user_id = call.data.replace("delete_user ", "")
    await sql_command_delete(user_id)
    await call.answer(text="Удалено!", show_alert=True)
    await bot.delete_message(call.from_user.id, call.message.message_id)


def register_user(dp: Dispatcher):
    dp.register_message_handler(delete_staff_by_city, commands=['all_user', 'Все_пользователи'])
    dp.register_callback_query_handler(complete_delete_staff, lambda c: c.data.startswith('delete_user '))
