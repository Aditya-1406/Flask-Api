import sqlite3

conn = sqlite3.connect("notes.db",check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes(
            id INTEGER PRIMARY KEY  AUTOINCREMENT,
            title VARCHAR(25) NOT NULL,
            description VARCHAR,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
               )

""")

conn.commit()
conn.close()