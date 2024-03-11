from aiogram import types, Dispatcher
from config import SuperAdmins, Admins
import buttons


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


def register(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
