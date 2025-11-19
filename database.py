import sqlite3

DB = "chat.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS chats(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_msg TEXT,
            bot_msg TEXT,
            ts TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_chat(user, bot):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO chats(user_msg, bot_msg, ts) VALUES (?, ?, datetime('now'))",
              (user, bot))
    conn.commit()
    conn.close()