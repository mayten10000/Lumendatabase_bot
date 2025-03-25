import sqlite3

def init_db():
    
    conn = sqlite3.connect("notifications.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site TEXT,
            notice_id INTEGER,
            title TEXT,
            description TEXT,
            response TEXT DEFAULT NULL,
            processed INTEGER DEFAULT 0
        )
    """)
    
    conn.commit()
    conn.close()

init_db()
