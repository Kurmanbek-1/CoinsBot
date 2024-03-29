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
                                      'Вы SuperAdmin‼️', reply_markup=buttons.startSuperAdmin)
            return
        else:
            await message.answer(text='Добро пожаловать в бот!\n'
                                      'Вы SuperAdmin‼️', reply_markup=buttons.startSuperAdmin)
    elif user_id in Admins:
        if user_data:
            await message.answer(text='Вы уже зарегистрированы! ✅ \n'
                                      'Посмотреть профиль ➡️ /my_profile\n'
                                      'Вы Admin‼️', reply_markup=buttons.startAdmin)
            return
        else:
            await message.answer(text='Добро пожаловать в бот!\n'
                                      'Вы Admin‼️', reply_markup=buttons.startAdmin)
    else:
        if user_data:
            if user_id in SuperAdmins:
                await message.answer(text='Вы уже зарегистрированы! ✅ \n'
                                          'Посмотреть профиль ➡️ /my_profile', reply_markup=buttons.startUser)
                return
        else:
            await message.answer(text='Добро пожаловать в бот!\n'
                                      'Для того чтобы начать, нажмите на команду ➡️ /registration',
                                 reply_markup=buttons.startUser)


async def back(message: types.Message):
    await message.answer('Вы возратились назад', reply_markup=buttons.startSuperAdmin)


def register(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(back, commands=['<_Назад'])
