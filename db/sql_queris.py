CREATE_TABLE_USER = """
    CREATE TABLE IF NOT EXISTS all_users
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_user VARCHAR(255),
    quantity VARCHAR(255)
    )
"""

INSERT_INTO_TABLE_USER = """
    INSERT INTO all_users(name_user, quantity) 
    VALUES (?, ?)
"""


SELECT_ALL_USER = """
    SELECT * FROM all_users
"""


CREATE_TABLE_USERS = """
    CREATE TABLE IF NOT EXISTS users
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_user VARCHAR(255),
    telegram_id VARCHAR(255)
    )
"""

INSERT_INTO_TABLE_USERS = """
    INSERT INTO users(name_user, telegram_id) 
    VALUES (?, ?)
"""


SELECT_ALL_USERS = """
    SELECT * FROM users
"""