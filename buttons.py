from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

startAdmin = ReplyKeyboardMarkup(resize_keyboard=True,
                                 one_time_keyboard=True,
                                 ).add(KeyboardButton('Начислить_баллы'))

startSuperAdmin = ReplyKeyboardMarkup(resize_keyboard=True,
                                 one_time_keyboard=True,
                                 ).add(KeyboardButton('/Все_пользователи!'),
                                       KeyboardButton('Начислить_баллы'))

startUser = ReplyKeyboardMarkup(resize_keyboard=True,
                                one_time_keyboard=True,
                                ).add(KeyboardButton('Мои_баллы!'))


cancel = ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True,
                                    ).add(KeyboardButton('Отмена'))