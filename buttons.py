from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

startAdmin = ReplyKeyboardMarkup(resize_keyboard=True,
                                 one_time_keyboard=True,
                                 ).add(KeyboardButton('Начислить_баллы'))

startSuperAdmin = ReplyKeyboardMarkup(resize_keyboard=True,
                                 one_time_keyboard=True,
                                 ).add(KeyboardButton('Начислить_баллы'),
                                       KeyboardButton('/Все_баллы!'),
                                       KeyboardButton('/Все_пользователи'))

startUser = ReplyKeyboardMarkup(resize_keyboard=True,
                                one_time_keyboard=True,
                                ).add(KeyboardButton('Мои_баллы!'),
                                      KeyboardButton('/MyProfile'))


cancel = ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True,
                                    ).add(KeyboardButton('Отмена'))