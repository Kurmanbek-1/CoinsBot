from aiogram import types, Dispatcher
from config import SuperAdmins, Admins
import buttons
from db.ORM import cursor


async def start(message: types.Message):
    if message.from_user.id in SuperAdmins:
        await message.answer(text='Добро пожаловать в бот!\n'
                                  'Вы SuperAdmin‼️', reply_markup=buttons.startSuperAdmin)

    elif message.from_user.id in Admins:
        await message.answer(text='Добро пожаловать в бот!\n'
                                  'Вы Admin‼️', reply_markup=buttons.startAdmin)

    else:
        await message.answer(text='Добро пожаловать в бот!\n'
                                  'Для того чтобы начать, нажмите на команду ➡️ /register',
                             reply_markup=buttons.startUser)


async def info(message: types.Message):
    if message.from_user.id in SuperAdmins:
        await message.answer(text=f"")

    elif message.from_user.id in Admins:
        await message.answer(text=f"")

    else:
        await message.answer(text=f"")


from db.ORM import cursor, db
from aiogram import types


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
                                            'Воспользуйтесь командой ➡️ /register.')
        return

    # Если пользователь найден в таблице 'users'
    user_name = user_data[1]  # Используем индекс 1, предполагая, что имя пользователя хранится во втором поле

    # Суммируем баллы пользователя из таблицы 'all_users'
    cursor.execute("SELECT SUM(quantity) FROM all_users WHERE name_user = ?", (user_name,))
    total_coins_result = cursor.fetchone()

    # Проверяем, что total_coins_result не равен None
    total_coins = total_coins_result[0] if total_coins_result is not None else 0

    photo_user = open('media/user.png', 'rb')
    photo_admin = open('media/admin.png', 'rb')

    # Проверяем, является ли пользователь администратором

    if total_coins is not None:
        if message.from_user.id in SuperAdmins:
            await message.answer_photo(photo=photo_admin, caption=f"Вы SuperAdmin!\n"
                                                                  f"=======================\n"
                                                                  f"Ваше имя - {user_name}\n"
                                                                  f"-----------------------\n"
                                                                  f"Ваши баллы - {total_coins}\n"
                                                                  f"=======================",
                                       reply_markup=buttons.startSuperAdmin)

        elif message.from_user.id in Admins:
            await message.answer_photo(photo=photo_admin, caption=f"Вы Admin!", reply_markup=buttons.startAdmin)

        else:
            # Если есть баллы для пользователя
            # Отправляем сообщение с общим количеством баллов пользователю
            await message.bot.send_photo(photo=photo_user,
                                         chat_id=telegram_id,
                                         caption=f"=======================\n"
                                                 f"Ваше имя - {user_name}\n"
                                                 f"-----------------------\n"
                                                 f"Ваши баллы - {total_coins}\n"
                                                 f"=======================")
    else:
        # Если пользователь не найден в таблице 'all_users'
        await message.bot.send_message(chat_id=telegram_id, text='Баллы не найдены.')


def register(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(info, commands=['info'])
    dp.register_message_handler(myprofile, commands=['my_profile'])
