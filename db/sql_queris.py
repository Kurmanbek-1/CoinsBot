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

SELECT_USER_BY_NAME = """
    SELECT * FROM users WHERE name_user = ?;
"""

CREATE_TABLE_INFO = """
    CREATE TABLE IF NOT EXISTS info
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_user VARCHAR(255),
    quantity VARCHAR(255),
    admin_id INTEGER,
    date VARCHAR(255), 
    action VARCHAR(255)
    )
"""

INSERT_INTO_TABLE_INFO = """
    INSERT INTO info(name_user, quantity, admin_id, date, action) 
    VALUES (?, ?, ?, ?, ?)
"""

CREATE_TABLE_ADMINS = """
    CREATE TABLE IF NOT EXISTS admins
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_admin VARCHAR(255),
    admin_id VARCHAR(255)
    )
"""

INSERT_INTO_TABLE_ADMINS = """
    INSERT INTO admins(name_admin, admin_id) 
    VALUES (?, ?)
"""

SELECT_ADMINS_NAME = """
    SELECT * FROM admins WHERE name_admin = ?;
"""