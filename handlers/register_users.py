from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons
from db.ORM import sql_insert_users, get_user_by_name  # Подставьте свои импорты для работы с базой данных
from config import Admins, SuperAdmins

# =======================================================================================================================

user_id = None


class RegisterUser(StatesGroup):
    name_user = State()


async def fsm_start(message: types.Message):
    await RegisterUser.name_user.set()
    await message.answer(text='Введите своё имя:\n(Только имя!)', reply_markup=buttons.cancel)


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_user'] = message.text
        data['telegram_id'] = message.chat.id

    # Проверка, существует ли пользователь с заданным именем в базе данных
    if await is_user_exists(data['name_user']):
        await message.answer('Пользователь с таким именем уже существует.\n'
                             'Пожалуйста, выберите другое имя.')
        return

    await RegisterUser.next()
    if message.from_user.id in SuperAdmins:
        await message.answer(text='Готово!\nВы теперь есть в базе данных!', reply_markup=buttons.startSuperAdmin)
    elif message.from_user in Admins:
        await message.answer(text='Готово!\nВы теперь есть в базе данных!', reply_markup=buttons.startAdmin)
    else:
        await message.answer(text='Готово!\nВы теперь есть в базе данных!', reply_markup=buttons.startUser)

    await sql_insert_users(state)
    await state.finish()


async def is_user_exists(name_user: str) -> bool:
    # Реальная логика проверки наличия пользователя с заданным именем в базе данных
    user = await get_user_by_name(name_user)
    return user is not None


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
def register_users(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, Text(equals="Отмена", ignore_case=True), state="*")
    dp.register_message_handler(fsm_start, commands=['registration'])
    dp.register_message_handler(load_name, state=RegisterUser.name_user)
