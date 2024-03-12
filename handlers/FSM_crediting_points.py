from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from collections import namedtuple
from config import bot, Admins, SuperAdmins
import buttons
from db.ORM import sql_insert_user, cursor


# =======================================================================================================================

class AddPoints(StatesGroup):
    name_user = State()
    quantity = State()
    submit = State()


async def fsm_start(message: types.Message):
    if message.from_user.id in Admins or SuperAdmins:
        await AddPoints.name_user.set()
        await message.answer("Имя пользователя?", reply_markup=buttons.cancel)
    else:
        await message.answer('Вы не админ!')


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_user'] = message.text
    await AddPoints.next()
    await message.answer(text='Количество баллов?')


async def load_quantity(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data['quantity'] = message.text

        query = "SELECT * FROM users WHERE name_user = ? AND telegram_id = ?"
        user_id = cursor.execute(query, (data['name_user'], message.from_user.id)).fetchone()

        if user_id:
            # Избегаем ошибки, если user_id не существует
            user_columns = cursor.description
            if user_columns:
                UserRecord = namedtuple('UserRecord', [col[0] for col in user_columns])
                user_id = UserRecord(*user_id)

                if message.from_user.id in SuperAdmins:
                    await message.answer(text=f"Готово!\n"
                                              f"Вы начислили - {data['quantity']} баллов пользователю {data['name_user']}",
                                         reply_markup=buttons.startSuperAdmin)
                else:
                    await message.answer(text=f"Готово!\n"
                                              f"Вы начислили - {data['quantity']} баллов пользователю {data['name_user']}",
                                         reply_markup=buttons.startAdmin)

                await message.bot.send_message(chat_id=user_id.telegram_id,
                                               text=f"Вам зачислили {data['quantity']} баллов!\n")
                await sql_insert_user(state)
                await state.finish()
            else:
                await message.answer(text="Не удалось получить описание столбцов из результата запроса.")
        else:
            await state.finish()

            if message.from_user.id in SuperAdmins:
                await message.answer(text=f"Такого пользователя нет!", reply_markup=buttons.startSuperAdmin)

            else:
                await message.answer(text=f"Такого пользователя нет!", reply_markup=buttons.startAdmin)

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


# =======================================================================================================================
def register_user_coins(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, Text(equals="Отмена", ignore_case=True), state="*")
    dp.register_message_handler(fsm_start, Text(equals="Начислить_баллы", ignore_case=True), state="*")
    dp.register_message_handler(load_name, state=AddPoints.name_user)
    dp.register_message_handler(load_quantity, state=AddPoints.quantity)
