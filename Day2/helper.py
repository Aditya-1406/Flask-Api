import sqlite3

DB = "notes.db"


class Helper:

    def __init__(self,DB = DB):
        self.conn = sqlite3.connect(DB,check_same_thread=False)
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
        return [dict(n) for n in notes]
    
    def post_notes(self,title,description):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO notes (title, description) VALUES (?, ?)",
            (title, description)
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_note(self,note_id):
        note = self.conn.execute("SELECT * FROM notes where id = ?", (note_id,)).fetchone()
        return dict(note) if note else None
    
    def update_note(self, note_id, title, description):
        self.conn.execute("""
            UPDATE notes
            SET title=?, description=?
            WHERE id=?
        """, (title, description, note_id))
        self.conn.commit()

    # ✅ DELETE
    def delete_note(self, note_id):
        self.conn.execute(
            "DELETE FROM notes WHERE id=?",
            (note_id,)
        )
        self.conn.commit()