import sqlite3
import os

def get_db_connection(db_path="database/nexus.db"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    # Automatically initialize DB tables if they don't exist
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            account_name TEXT NOT NULL,
            refresh_token TEXT,
            status TEXT DEFAULT 'active',
            last_used TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            niche TEXT NOT NULL,
            title TEXT,
            script TEXT,
            video_path TEXT,
            status TEXT DEFAULT 'generated',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posting_schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id INTEGER,
            account_id INTEGER,
            scheduled_time TIMESTAMP,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY(video_id) REFERENCES videos(id),
            FOREIGN KEY(account_id) REFERENCES accounts(id)
        )
    ''')
    conn.commit()
    return conn

def init_db(db_path="database/nexus.db"):
    conn = get_db_connection(db_path)
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
