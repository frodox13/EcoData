import sqlite3

DB_NAME = "ecodata.db"

def init_db():
    # Inicializa la base de datos y crea las tablas si no existen.
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash BLOB NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            indicator TEXT NOT NULL,
            query_date TEXT NOT NULL,
            value_date TEXT NOT NULL DEFAULT '',
            result TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

def add_user(username: str, password_hash: bytes) -> bool:
    # Agrega un nuevo usuario a la base de datos.
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user(username: str):
    # Obtiene un usuario por nombre de usuario.
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def save_query(user_id: int, indicator: str, query_date: str, value_date: str, result: str):
    # Guarda una consulta realizada por un usuario, incluyendo la fecha de actualización del valor.
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO queries (user_id, indicator, query_date, value_date, result) VALUES (?, ?, ?, ?, ?)",
        (user_id, indicator, query_date, value_date, result)
    )
    conn.commit()
    conn.close()

def get_user_queries(user_id: int):
    # Obtiene todas las consultas realizadas por un usuario.
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT indicator, query_date, value_date, result FROM queries WHERE user_id = ?", (user_id,))
    queries = cursor.fetchall()
    conn.close()
    return queries

def get_all_queries():
    # Obtiene todas las consultas realizadas en el sistema (para administrador), incluyendo el nombre de usuario y value_date.
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT users.username, queries.indicator, queries.query_date, queries.value_date, queries.result
        FROM queries
        JOIN users ON queries.user_id = users.id
    """)
    queries = cursor.fetchall()
    conn.close()
    return queries