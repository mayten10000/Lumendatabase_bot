import sqlite3

def read_all_notifications():
    
    conn = sqlite3.connect('notifications.db')
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM notifications")

        rows = cursor.fetchall()

        for row in rows:

            print(row)  

    except sqlite3.Error as e:
        
        print(f"Ошибка при чтении базы данных: {e}")
        
    finally:
        
        conn.close()

read_all_notifications()
