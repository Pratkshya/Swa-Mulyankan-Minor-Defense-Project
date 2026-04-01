import sqlite3

DB = "app.db"

# -----------------------
# DATABASE CONNECTION
# -----------------------
def get_db():
    return sqlite3.connect(DB)


# -----------------------
# INIT DATABASE
# -----------------------
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # RESULTS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        mastery REAL,
        gap INTEGER,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()


# -----------------------
# USER FUNCTIONS
# -----------------------
def create_user(username, password):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )

    conn.commit()
    conn.close()


def get_user(username):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()

    return user


# -----------------------
# RESULT FUNCTIONS
# -----------------------
def save_result(user_id, mastery, gap, status):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO results (user_id, mastery, gap, status) VALUES (?, ?, ?, ?)",
        (user_id, mastery, gap, status)
    )

    conn.commit()
    conn.close()


def get_results(user_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT mastery, gap, status FROM results WHERE user_id=?",
        (user_id,)
    )

    results = cursor.fetchall()
    conn.close()

    return results