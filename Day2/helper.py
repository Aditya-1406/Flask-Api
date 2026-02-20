import sqlite3

DB = "notes.db"


class Helper:

    def __init__(self,DB):
        self.conn = sqlite3.connect(DB)
        self.conn.row_factory = sqlite3.Row
        self.create_table()

    def create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS notes(
            id INTEGER PRIMARY KEY  AUTOINCREMENT,
            title VARCHAR(25) NOT NULL,
            description VARCHAR,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
               )
""")
        self.conn.commit()

    def get_notes(self):
        notes = self.conn.execute("SELECT * FROM notes").fetchall()
        return (dict(n) for n in notes)