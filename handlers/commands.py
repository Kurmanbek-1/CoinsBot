from aiogram import types, Dispatcher
from config import SuperAdmins, Admins
import buttons
from db.ORM import cursor


async def start(message: types.Message):
    user_id = message.from_user.id
    users_query = "SELECT * FROM users WHERE telegram_id = ?"
    user_data = cursor.execute(users_query, (user_id,)).fetchone()

    if user_id in SuperAdmins:
        if user_data:
            await message.answer(text='Вы уже зарегистрированы! ✅ \n'
                                      'Посмотреть профиль ➡️ /my_profile\n'
                                      'Вы SuperAdmin‼️')
            return
        else:
            await message.answer(text='Добро пожаловать в бот!\n'
                                      'Вы SuperAdmin‼️', reply_markup=buttons.startSuperAdmin)
    elif user_id in Admins:
        if user_data:
            await message.answer(text='Вы уже зарегистрированы! ✅ \n'
                                      'Посмотреть профиль ➡️ /my_profile\n'
                                      'Вы Admin‼️')
            return
        else:
            await message.answer(text='Добро пожаловать в бот!\n'
                                      'Вы Admin‼️', reply_markup=buttons.startAdmin)
    else:
        if user_data:
            await message.answer(text='Вы уже зарегистрированы! ✅ \n'
                                      'Посмотреть профиль ➡️ /my_profile')
            return
        else:
            await message.answer(text='Добро пожаловать в бот!\n'
                                      'Для того чтобы начать, нажмите на команду ➡️ /registration',
                                 reply_markup=buttons.startUser)


async def info(message: types.Message):
    if message.from_user.id in SuperAdmins:
        await message.answer(text=f"")

    elif message.from_user.id in Admins:
        await message.answer(text=f"")

    else:
        await message.answer(text=f"")


async def myprofile(message: types):
    # Получаем telegram_id пользователя из сообщения
    telegram_id = message.from_user.id

    # Проверяем, существует ли пользователь в таблице 'users'
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    user_data = cursor.fetchone()

    # Если пользователь не найден в таблице 'users'
    if user_data is None:
        await message.bot.send_message(chat_id=telegram_id,
                                       text='Вы не зарегистрированы в системе как пользователь.\n'
                                            'Воспользуйтесь командой ➡️ /registration.')
        return

    # Если пользователь найден в таблице 'users'
    user_name = user_data[1]  # Используем индекс 1, предполагая, что имя пользователя хранится во втором поле

    # Суммируем баллы пользователя из таблицы 'all_users'
    # Суммируем баллы пользователя из таблицы 'all_users'
    # Суммируем баллы пользователя из таблицы 'all_users'
    cursor.execute("SELECT SUM(quantity) FROM all_users WHERE name_user = ?", (user_name,))
    total_coins_result = cursor.fetchone()

    # Проверяем, что total_coins_result не равен None
    total_coins = total_coins_result[0] if total_coins_result is not None else 0

    photo = open('media/admin.png', 'rb')

    # Проверяем, является ли пользователь администратором
    if message.from_user.id in SuperAdmins:
        await message.answer_photo(photo=photo, caption=f"Вы SuperAdmin❗️\n"
                                                        f"=======================\n"
                                                        f"Name - {user_name}\n"
                                                        f"-----------------------\n"
                                                        f"AntsCoin - {total_coins}\n"
                                                        f"=======================",
                                   reply_markup=buttons.startSuperAdmin)

    elif message.from_user.id in Admins:
        await message.answer_photo(photo=photo, caption=f"Вы Admin❗️\n"
                                                        f"=======================\n"
                                                        f"Name - {user_name}\n"
                                                        f"-----------------------\n"
                                                        f"AntsCoin - {total_coins}\n",
                                   reply_markup=buttons.startAdmin)

    else:
        # Проверяем, есть ли баллы для пользователя
        if total_coins is not None:
            await message.bot.send_photo(photo=photo,
                                         chat_id=telegram_id,
                                         caption=f"=======================\n"
                                                 f"Name - {user_name}\n"
                                                 f"-----------------------\n"
                                                 f"AntsCoin - {total_coins}\n"
                                                 f"=======================")
        else:
            # Если баллов нет, отобразить только имя с 0 баллами
            await message.bot.send_photo(photo=photo,
                                         chat_id=telegram_id,
                                         caption=f"=======================\n"
                                                 f"Name - {user_name}\n"
                                                 f"-----------------------\n"
                                                 f"AntsCoin - 0\n"
                                                 f"=======================")


def register(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(info, commands=['info'])
    dp.register_message_handler(myprofile, commands=['my_profile'])
