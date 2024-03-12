from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from config import bot, Admins, SuperAdmins
import buttons
from db.ORM import sql_insert_users

# =======================================================================================================================

user_id = None


class RegisterUser(StatesGroup):
    name_user = State()


async def fsm_start(message: types.Message):
    if message.from_user.id in Admins:
        await message.answer("Вы уже являетесь админом!", reply_markup=buttons.startAdmin)

    elif message.from_user.username in SuperAdmins:
        await message.answer("Вы уже являетесь админом!", reply_markup=buttons.startSuperAdmin)

    else:
        await RegisterUser.name_user.set()
        await message.answer(text='Ваше имя?\n'
                                  '(Только имя!)')


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_user'] = message.text
        data['telegram_id'] = message.chat.id
    await RegisterUser.next()
    await message.answer(text='Готово!\n'
                              'Вы теперь есть в базе данных!')

    await sql_insert_users(state)
    await state.finish()


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Отменено!', reply_markup=None)


# =======================================================================================================================
def register_users(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, Text(equals="Отмена", ignore_case=True), state="*")
    dp.register_message_handler(fsm_start, commands=['register'])
    dp.register_message_handler(load_name, state=RegisterUser.name_user)
