from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons
from db.ORM import sql_insert_admins, get_admins_name, sql_insert_users, get_admins_id_name
from config import Admins, SuperAdmins


# =======================================================================================================================


class RegisterAdmin(StatesGroup):
    name_user = State()


async def fsm_start(message: types.Message):
    telegram_id = message.from_user.id
    if message.from_user.id in SuperAdmins or Admins:
        if await is_user_id_exists(telegram_id):
            await message.answer('Вы уже проходили регистрацию!')
            return
        else:
            await RegisterAdmin.name_user.set()
            await message.answer(text='Введите своё имя:\n(Только имя!)', reply_markup=buttons.cancel)
    else:
        await message.answer('Вы не являетесь админом!')


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data_admin:
        data_admin['name_user'] = message.text
        data_admin['telegram_id'] = message.chat.id

    # Проверка, существует ли пользователь с заданным именем в базе данных
    if await is_user_exists(data_admin['name_user']):
        await message.answer('Пользователь с таким именем уже существует.\n'
                             'Пожалуйста, выберите другое имя.')
        return

    await RegisterAdmin.next()

    # Запись в таблицу админов
    await sql_insert_admins(state)

    # Запись в таблицу пользователей
    await sql_insert_users(state)

    if message.from_user.id in SuperAdmins:
        await message.answer(text='Готово!\nВы теперь есть в базе данных!', reply_markup=buttons.startSuperAdmin)
    elif message.from_user in Admins:
        await message.answer(text='Готово!\nВы теперь есть в базе данных!', reply_markup=buttons.startAdmin)

    await state.finish()


async def is_user_exists(name_user: str) -> bool:
    # Реальная логика проверки наличия пользователя с заданным именем в базе данных
    user = await get_admins_name(name_user)
    return user is not None


async def is_user_id_exists(telegram_id: str) -> bool:
    # Реальная логика проверки наличия пользователя с заданным именем в базе данных
    user_id = await get_admins_id_name(telegram_id)
    return user_id is not None


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        if message.from_user.id in SuperAdmins:
            await message.answer('Отменено!', reply_markup=buttons.startSuperAdmin)
        elif message.from_user in Admins:
            await message.answer('Отменено!', reply_markup=buttons.startAdmin)
        else:
            await message.answer('Отменено!', reply_markup=buttons.startUser)


# =======================================================================================================================
def register_admin(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, Text(equals="Отмена", ignore_case=True), state="*")
    dp.register_message_handler(fsm_start, commands=['registration_admin'])
    dp.register_message_handler(load_name, state=RegisterAdmin.name_user)
