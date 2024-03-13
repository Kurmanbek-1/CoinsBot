import sqlite3
from db import sql_queris

# db = sqlite3.connect("AdminPanelBot/db.sqlite3")
db = sqlite3.connect("db/db.sqlite3")
cursor = db.cursor()


async def sql_create():
    if db:
        print("База Бишкек подключена!")
    cursor.execute(sql_queris.CREATE_TABLE_USER)
    cursor.execute(sql_queris.CREATE_TABLE_USERS)
    db.commit()


async def sql_insert_user(state):
    async with state.proxy() as data:
        cursor.execute(sql_queris.INSERT_INTO_TABLE_USER, (
            data.get('name_user'),
            data.get('quantity')
        ))
        db.commit()


async def sql_insert_users(state):
    async with state.proxy() as data:
        cursor.execute(sql_queris.INSERT_INTO_TABLE_USERS, (
            data.get('name_user'),
            data.get('telegram_id')
        ))
        db.commit()


async def get_user_by_name(name_user):
    cursor.execute(sql_queris.SELECT_USER_BY_NAME, (name_user,))
    return cursor.fetchone()
