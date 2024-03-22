from aiogram import Dispatcher, types
from db.ORM import cursor
from config import SuperAdmins
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import buttons


class ReportState(StatesGroup):
    CHOOSING_USER = State()
    VIEWING_REPORT = State()


async def start_report(message: types.Message):
    if message.from_user.id in SuperAdmins:
        employees = cursor.execute("SELECT DISTINCT name_user FROM info").fetchall()

        if not employees:
            await message.answer("Список пуст!")
            return

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(KeyboardButton("Отмена"))
        keyboard.add(*[KeyboardButton(user[0]) for user in employees])

        await message.answer("Выберите пользователя:", reply_markup=keyboard)
        await ReportState.CHOOSING_USER.set()
    else:
        await message.answer("У вас нет прав к этой команде!")


async def process_user_choice(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        selected_user = message.text
        data['selected_user'] = selected_user

        employee_info = cursor.execute("SELECT * FROM info WHERE name_user = ?", (selected_user,)).fetchall()

        if not employee_info:
            await message.answer(f"Нет информации о пользователе {selected_user}")
            await state.finish()
            return

        for user in employee_info:
            telegram_id = user[3]
            admin_info = cursor.execute("SELECT name_user FROM admins WHERE telegram_id = ?", (telegram_id,)).fetchone()
            admin_name = admin_info[0] if admin_info else "Неизвестный админ"

            status = user[5] if user[5] is not None else "Без статуса"  # Проверяем наличие статуса

            await message.answer(text=f"Кому - {user[1]}\n"
                                      f"Кол.AnstCoin'ов - {user[2]}\n"
                                      f"От - {admin_name}\n"
                                      f"Когда - {user[4]}\n"
                                      f"Status - {status}")

        # await ReportState.VIEWING_REPORT.set()


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        if message.from_user.id in SuperAdmins:
            await message.answer('Отменено!', reply_markup=buttons.startSuperAdmin)
        else:
            await message.answer('Отменено!', reply_markup=buttons.startAdmin)


def register_report(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, Text(equals="Отмена", ignore_case=True), state="*")
    dp.register_message_handler(start_report, commands=['report', 'Отчёт'])
    dp.register_message_handler(process_user_choice, state=ReportState.CHOOSING_USER)
