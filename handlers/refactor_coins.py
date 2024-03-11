from db.ORM import cursor, db
from aiogram import Dispatcher, types
from config import dp


async def update_user_coins(message: types.Message):
    # Получаем telegram_id пользователя из сообщения
    telegram_id = message.from_user.id

    # Проверяем, существует ли пользователь в таблице 'users'
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    user_data = cursor.fetchone()

    if user_data:
        # Если пользователь найден в таблице 'users'
        user_name = user_data[1]  # Используем индекс 1, предполагая, что имя пользователя хранится во втором поле

        if not user_name:
            await message.answer('Не удалось определить имя пользователя.')
            return

        # Посылаем запрос пользователю о вводе нового значения
        await message.answer('Введите новое количество баллов:')

        # Регистрируем обработчик для ожидания следующего сообщения от пользователя
        dp.register_message_handler(process_new_quantity, state="*", content_types=types.ContentType.TEXT,
                                    chat_id=telegram_id, user_id=telegram_id, is_admin=False, is_forwarded=False,
                                    regexp=None)
    else:
        # Если пользователь не найден в таблице 'users'
        await message.answer('Вы не зарегистрированы в системе.')


async def process_new_quantity(message: types.Message):
    try:
        # Пробуем преобразовать ответ в число
        new_quantity = int(message.text)

        # Получаем данные о пользователе из сообщения
        telegram_id = message.from_user.id
        user_name = message.text  # предполагаем, что имя пользователя содержится в тексте сообщения

        # Обновляем количество баллов пользователя в таблице 'all_users'
        cursor.execute("UPDATE all_users SET quantity = ? WHERE name_user = ?", (new_quantity, user_name))

        # Подтверждаем изменения в базе данных
        db.commit()

        # Отправляем сообщение с подтверждением обновления
        await message.answer(f'Количество ваших баллов было обновлено: {new_quantity}')
    except ValueError:
        # Если не удалось преобразовать в число
        await message.answer('Введите корректное число.')


def register_update(dp: Dispatcher):
    dp.register_message_handler(update_user_coins, commands=['обновить_баллы', 'update_coins'], state="*")
