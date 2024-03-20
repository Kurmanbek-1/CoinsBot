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
    cursor.execute(sql_queris.CREATE_TABLE_INFO)
    cursor.execute(sql_queris.CREATE_TABLE_ADMINS)
    db.commit()


async def sql_insert_user(state):
    async with state.proxy() as data:
        cursor.execute(sql_queris.INSERT_INTO_TABLE_USER, (
            data.get('name_user'),
            data.get('quantity'),
            data.get('admin_id'),
            data.get('date')
        ))
        db.commit()


async def sql_insert_users(state):
    async with state.proxy() as data:
        cursor.execute(sql_queris.INSERT_INTO_TABLE_USERS, (
            data.get('name_user'),
            data.get('telegram_id')
        ))
        db.commit()


async def sql_insert_admins(state):
    async with state.proxy() as data_admin:
        cursor.execute(sql_queris.INSERT_INTO_TABLE_ADMINS, (
            data_admin.get('name_user'),
            data_admin.get('telegram_id')
        ))
        db.commit()


async def get_user_by_name(name_user):
    cursor.execute(sql_queris.SELECT_USER_BY_NAME, (name_user,))
    return cursor.fetchone()


async def get_user_id_by_name(telegram_id):
    cursor.execute(sql_queris.SELECT_USER_ID_BY_NAME, (telegram_id,))
    return cursor.fetchone()


async def get_admins_name(name_admin):
    cursor.execute(sql_queris.SELECT_ADMINS_NAME, (name_admin,))
    return cursor.fetchone()


async def get_admins_id_name(telegram_id):
    cursor.execute(sql_queris.SELECT_ADMINS_ID_NAME, (telegram_id,))
    return cursor.fetchone()