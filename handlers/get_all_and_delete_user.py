from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.ORM import cursor, db
from config import bot, SuperAdmins


async def send_users(message: types.Message):
    if message.from_user.id in SuperAdmins or message.from_user.id == bot.id:
        # Получите данные о пользователях из базы данных (замените этот код на ваш запрос к базе данных)
        cursor.execute("SELECT name_user, SUM(quantity) FROM all_users GROUP BY name_user")
        user_scores = cursor.fetchall()

        if not user_scores:
            await message.answer("Список пуст!")
            return

        for user in user_scores:
            user_name = user[0]
            user_quantity = user[1]

            keyboard = InlineKeyboardMarkup()
            delete_button = InlineKeyboardButton("Удалить", callback_data=f"delete_user_{user_name}")
            keyboard.add(delete_button)

            user_text = f"{user_name} - {user_quantity} баллов"
            await message.answer(user_text, reply_markup=keyboard)
    else:
        await message.answer('У вас недостаточно прав для этой команды!')


async def delete_user(callback_query: types.CallbackQuery):
    user_name = callback_query.data.split('_')[2]  # Получаем имя пользователя

    try:
        cursor.execute("DELETE FROM all_users WHERE name_user = ?", (user_name,))
        db.commit()

        print(f"Пользователь {user_name} успешно удален.")

        await bot.answer_callback_query(callback_query.id, text=f"Пользователь {user_name} удален.")
        await bot.delete_message(callback_query.id, callback_query.message.message_id)
    except Exception as e:
        print(f"Ошибка при удалении пользователя: {e}")
        await bot.answer_callback_query(callback_query.id, text=f"Ошибка при удалении пользователя: {e}")


def register_delete(dp: Dispatcher):
    dp.register_message_handler(send_users, commands=["Все_баллы!", "all_coins"])
    dp.register_callback_query_handler(delete_user, lambda c: c.data.startswith('delete_user_'))
