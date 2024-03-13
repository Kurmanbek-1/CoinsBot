from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from db.ORM import cursor, db
from config import bot, SuperAdmins, Admins
import buttons


# ...

class EditPoints(StatesGroup):
    name_user = State()
    new_quantity = State()


# ...

async def fsm_start_edit(message: types.Message):
    if message.from_user.id in SuperAdmins:
        await EditPoints.name_user.set()
        await message.answer("Имя пользователя для редактирования?", reply_markup=buttons.cancel)

    else:
        await message.answer('У вас нет прав к этой команде!')


# ...

async def load_name_for_edit(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_user'] = message.text
    await EditPoints.next()
    await message.answer(text='Новое количество AntsCoin?')


# ...

async def load_new_quantity(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data['new_quantity'] = message.text

        update_query = "UPDATE all_users SET quantity = ? WHERE name_user = ?"
        cursor.execute(update_query, (data['new_quantity'], data['name_user']))
        cursor.connection.commit()  # Фиксация изменений в базе данных

        await message.answer(text=f"Готово!\n"
                                  f"Вы изменили количество AntsCoin для пользователя {data['name_user']} "
                                  f"на {data['new_quantity']} AntsCoin",
                             reply_markup=buttons.startSuperAdmin)

        # Отправляем уведомление пользователю
        user_info = cursor.execute("SELECT telegram_id FROM users WHERE name_user = ?", (data['name_user'],)).fetchone()
        if user_info:
            telegram_id = user_info[0]
            await bot.send_message(telegram_id, f"Ваш баланс был изменен на {data['new_quantity']} AntsCoin.")
        else:
            print(f"User {data['name_user']} not found in the users table.")

        await state.finish()
    else:
        await message.answer('Введите числами!')


# ...

async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Отменено!', reply_markup=buttons.startSuperAdmin)


# ...

def register_edit(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, Text(equals="Отмена", ignore_case=True), state="*")
    dp.register_message_handler(fsm_start_edit, commands=["Редактировать_AntsCoin"])
    dp.register_message_handler(load_name_for_edit, state=EditPoints.name_user)
    dp.register_message_handler(load_new_quantity, state=EditPoints.new_quantity)
