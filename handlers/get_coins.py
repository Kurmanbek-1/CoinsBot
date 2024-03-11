from db.ORM import cursor
from aiogram import Dispatcher, types


async def get_user_coins(message: types.Message):
    # Получаем telegram_id пользователя из сообщения
    telegram_id = message.from_user.id

    # Проверяем, существует ли пользователь в таблице 'users'
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    user_data = cursor.fetchone()

    if user_data:
        # Если пользователь найден в таблице 'users'
        user_name = user_data[1]  # Используем индекс 1, предполагая, что имя пользователя хранится во втором поле
        user_id = user_data[0]  # Используем индекс 0 для telegram_id

        # Суммируем баллы пользователя из таблицы 'all_users'
        cursor.execute("SELECT SUM(quantity) FROM all_users WHERE name_user = ?", (user_name,))
        total_coins = cursor.fetchone()[0]  # Используем индекс 0 для получения суммы

        if total_coins is not None:
            # Если есть баллы для пользователя
            # Отправляем сообщение с общим количеством баллов пользователю
            await message.bot.send_message(chat_id=telegram_id, text=f'У вас {total_coins} баллов')
        else:
            # Если пользователь не найден в таблице 'all_users'
            await message.bot.send_message(chat_id=telegram_id, text='Баллы не найдены.')
    else:
        # Если пользователь не найден в таблице 'users'
        await message.bot.send_message(chat_id=telegram_id, text='Вы не зарегистрированы в системе.')


async def update_user_coins(message: types.Message, new_quantity: int):
    # Получаем telegram_id пользователя из сообщения
    telegram_id = message.from_user.id

    # Проверяем, существует ли пользователь в таблице 'users'
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    user_data = cursor.fetchone()

    if user_data:
        # Если пользователь найден в таблице 'users'
        user_name = user_data[1]  # Используем индекс 1, предполагая, что имя пользователя хранится во втором поле
        user_id = user_data[0]  # Используем индекс 0 для telegram_id

        # Обновляем количество баллов пользователя в таблице 'all_users'
        cursor.execute("UPDATE all_users SET quantity = ? WHERE name_user = ?", (new_quantity, user_name))

        # Подтверждаем изменения в базе данных
        db.commit()

        # Отправляем сообщение с подтверждением обновления
        await message.bot.send_message(chat_id=telegram_id,
                                       text=f'Количество ваших баллов было обновлено: {new_quantity}')
    else:
        # Если пользователь не найден в таблице 'users'
        await message.bot.send_message(chat_id=telegram_id, text='Вы не зарегистрированы в системе.')


def register_get(dp: Dispatcher):
    dp.register_message_handler(get_user_coins, commands=['Мои_баллы!', 'my_coins'])
    dp.register_message_handler(update_user_coins, commands=['обновить_баллы', 'update_coins'])
