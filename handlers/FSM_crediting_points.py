from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from db.ORM import sql_insert_user, cursor  # Убедитесь, что пути импорта правильные
import buttons
from config import bot, Admins, SuperAdmins


# Определение клавиатуры для выбора пользователя
async def get_users_keyboard():
    users_query = "SELECT name_user FROM users"
    users_data = cursor.execute(users_query).fetchall()

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3).add(
        KeyboardButton('Отмена'))

    for user_data in users_data:
        user_name = user_data[0]
        keyboard.insert(KeyboardButton(user_name))

    return keyboard


class AddPoints(StatesGroup):
    name_user = State()
    quantity = State()
    submit = State()


async def fsm_start(message: types.Message):
    if message.from_user.id in Admins or message.from_user.id in SuperAdmins:
        keyboard = await get_users_keyboard()
        await AddPoints.name_user.set()
        await message.answer("Выберите пользователя из списка:", reply_markup=keyboard)
    else:
        await message.answer('Вы не админ!')


async def send_notification_to_all(message: types.Message, user_name: str, amount: int):
    users_query = "SELECT telegram_id FROM users WHERE telegram_id != ?"
    users_data = cursor.execute(users_query, (message.from_user.id,)).fetchall()

    for user_data in users_data:
        user_id = user_data[0]
        await bot.send_message(chat_id=user_id, text=f"Пользователю {user_name} зачислено {amount} AntsCoin'ов! ✅")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_user'] = message.text

    # Проверяем, что выбранное имя присутствует в клавиатуре
    users_query = "SELECT name_user FROM users"
    users_data = cursor.execute(users_query).fetchall()
    available_user_names = [user_data[0] for user_data in users_data]

    if data['name_user'] not in available_user_names:
        await message.answer("Выберите пользователя из списка.")
        return

    await AddPoints.next()
    await message.answer(text='Количество AntsCoin?', reply_markup=buttons.cancel)


async def load_quantity(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data['quantity'] = int(message.text)

        users_query = "SELECT * FROM users WHERE name_user = ?"
        users_data = cursor.execute(users_query, (data['name_user'],)).fetchone()

        print("Данные пользователей:", users_data)

        if users_data:
            # Извлечение данных из таблицы users
            name_user = users_data[1]
            telegram_id = users_data[2]

            # Запрос к таблице all_users
            all_users_query = "SELECT * FROM all_users WHERE name_user = ?"
            all_users_data = cursor.execute(all_users_query, (name_user,)).fetchone()

            if all_users_data:
                # Если пользователь уже существует, обновляем quantity
                existing_quantity = int(all_users_data[2])
                new_quantity = existing_quantity + data['quantity']

                update_all_users_query = "UPDATE all_users SET quantity = ? WHERE name_user = ?"
                cursor.execute(update_all_users_query, (new_quantity, name_user))
            else:
                # Если пользователь новый, добавляем запись
                insert_all_users_query = "INSERT INTO all_users(name_user, quantity) VALUES (?, ?)"
                cursor.execute(insert_all_users_query, (name_user, data['quantity']))
                new_quantity = data['quantity']

            cursor.connection.commit()

            # Отправка уведомления всем пользователям, кроме того, кому начисляются монеты
            await send_notification_to_all(message, name_user, data['quantity'])

            if message.from_user.id in SuperAdmins:
                await message.answer(text=f"Готово! ✅\n"
                                          f"Пользователь - {name_user}\n"
                                          f"AntsCoin'ов переведено - {data['quantity']}",
                                     reply_markup=buttons.startSuperAdmin)
            else:
                await message.answer(text=f"Готово! ✅\n"
                                          f"Пользователь - {name_user}\n"
                                          f"AntsCoin'ов переведено - {data['quantity']}",
                                     reply_markup=buttons.startAdmin)

            await bot.send_message(chat_id=telegram_id, text=f"Вам зачислено {data['quantity']} AntsCoin! ✅. "
                                                             f"Итого у вас {new_quantity} AntsCoin'ов")

            await state.finish()
        else:
            await message.answer(text="Такого пользователя нет!")
    else:
        await message.answer('Введите числами!')


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        if message.from_user.id in SuperAdmins:
            await message.answer('Отменено!', reply_markup=buttons.startSuperAdmin)
        else:
            await message.answer('Отменено!', reply_markup=buttons.startAdmin)


def register_user_coins(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, Text(equals="Отмена", ignore_case=True), state="*")
    dp.register_message_handler(fsm_start, Text(equals="Начислить_AntsCoin", ignore_case=True), state="*")
    dp.register_message_handler(load_name, state=AddPoints.name_user)
    dp.register_message_handler(load_quantity, state=AddPoints.quantity)
