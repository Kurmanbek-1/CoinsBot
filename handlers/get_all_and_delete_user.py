from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.ORM import cursor, db
from config import bot, SuperAdmins


async def sql_command_delete(user_id):
    cursor.execute("DELETE FROM all_users WHERE id = ?", (user_id,))
    db.commit()


async def send_users(message: types.Message):
    if message.from_user.id in SuperAdmins:
        employees = cursor.execute("SELECT name_user, SUM(quantity) FROM all_users GROUP BY name_user").fetchall()
        if not employees:
            await message.answer("Список пуст!")
        else:
            keyboard = InlineKeyboardMarkup()
            for user in employees:
                user_name = user[0]
                user_quantity = user[1]

                callback_data = f"delete_user_{user_name.replace(' ', '_')}"
                print(f"Callback data for user {user_name}: {callback_data}")

                keyboard.add(InlineKeyboardButton("Удалить", callback_data=callback_data))

            # Используем types.InputFile для передачи изображения
            photo_user = types.InputFile("media/img.png")

            await message.answer_photo(photo=photo_user, caption="Список пользователей:", reply_markup=keyboard)
    else:
        await message.answer("У вас нет прав к этой команде!")


async def complete_delete_staff(call: types.CallbackQuery):
    user_name = call.data.replace("delete_user_", "").replace('_', ' ')
    user_info = cursor.execute("SELECT id FROM all_users WHERE name_user = ?", (user_name,)).fetchone()

    if user_info:
        user_id = user_info[0]
        await sql_command_delete(user_id)
        await call.answer(text="Удалено!", show_alert=True)
        await bot.delete_message(call.from_user.id, call.message.message_id)
    else:
        print(f"Invalid user ID (not found in the database): {user_name}")
        await call.answer(text="Ошибка при удалении пользователя", show_alert=True)


def register_delete(dp: Dispatcher):
    dp.register_message_handler(send_users, commands=["Все_AntsCoin!", "all_AntsCoin"])
    dp.register_callback_query_handler(complete_delete_staff, lambda c: c.data.startswith('delete_user_'))
