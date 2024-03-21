from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

startAdmin = ReplyKeyboardMarkup(resize_keyboard=True,
                                 one_time_keyboard=True,
                                 row_width=2,
                                 ).add(KeyboardButton('Начислить_AntsCoin'))

startSuperAdmin = ReplyKeyboardMarkup(resize_keyboard=True,
                                 one_time_keyboard=True,
                                      row_width=2,
                                 ).add(KeyboardButton('Начислить_AntsCoin'),
                                       KeyboardButton('Редактировать_AntsCoin'),
                                       KeyboardButton('/Все_пользователи'),
                                       KeyboardButton('/Все_AntsCoin!'),
                                       KeyboardButton('/Отчёт'))

startUser = ReplyKeyboardMarkup(resize_keyboard=True,
                                one_time_keyboard=True,
                                ).add(KeyboardButton('/my_profile'))


cancel = ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True,
                                    ).add(KeyboardButton('Отмена'))