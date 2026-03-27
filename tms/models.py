import tms.db as db

class Tester:
    table = "testers"

    def __init__(self, name: str, level: str):
        self.name = name
        self.level = level
        self.id = None

    @staticmethod
    def create_table(db: 'db.SQLiteDatabase'):
        db.execute(f"CREATE TABLE IF NOT EXISTS {Tester.table} (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, level TEXT)")

    def save_to_table(self, db: 'db.SQLiteDatabase') -> 'Tester':
        self.id = db.execute(f"INSERT INTO {Tester.table} (name, level) VALUES (?, ?)", (self.name, self.level))
        return self

    @staticmethod
    def get_from_table(db: 'db.SQLiteDatabase', name) -> 'Tester':
        row = db.execute(f"SELECT * FROM {Tester.table} WHERE name = ?", (name,))[0]
        return Tester.from_row(row)

    def update_level_in_table(self, db: 'db.SQLiteDatabase', level):
        db.execute(f"UPDATE {self.table} SET level = ? WHERE id = ?", (level, self.id))

class Bug:
    table = "bugs"

    def __init__(self, title: str, description: str, created_by: int):
        self.title = title
        self.description = description
        self.status = "open"
        self.created_by = created_by
        self.id = None

    @staticmethod
    def create_table():
        return f"CREATE TABLE IF NOT EXISTS {Bug.table} (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT, status TEXT, created_by INTEGER)"

    def save(self, conn):
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {self.table} (title, description, status, created_by) VALUES (?, ?, ?, ?)",
                      (self.title, self.description, self.status, self.created_by))
        conn.commit()
        self.id = cursor.lastrowid

    def update_status(self, conn, status):
        self.status = status
        cursor = conn.cursor()
        cursor.execute(f"UPDATE {self.table} SET status = ? WHERE id = ?", (status, self.id))
        conn.commit()

    @staticmethod
    def get_all(conn):
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {Bug.table}")
        bugs = []
        for row in cursor.fetchall():
            b = Bug(row[1], row[2], row[4])
            b.status = row[3]
            b.id = row[0]
            bugs.append(b)
        return bugs