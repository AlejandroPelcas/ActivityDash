import sqlite3

DB_NAME = "strava.db"

def get_db() -> None:
    """ Start connection to db """
    return sqlite3.connect(DB_NAME)

def init_db() -> None:
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS token (
            id INTEGER PRIMARY KEY,
            access_token TEXT,
            refresh_token TEXT,
            expires_at INTEGER
            )
    """)

    conn.commit()
    conn.close()

