import sqlite3
import os


class SQLiteDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        self.conn = sqlite3.connect(self.db_path)

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def execute(self, sql: str, params: tuple = ()):
        if not self.conn:
            self.connect()

        cursor = self.conn.cursor()
        cursor.execute(sql, params)

        sql_upper = sql.strip().upper()

        if sql_upper.startswith('SELECT'):
            result = cursor.fetchall()
            cursor.close()
            return result
        else:
            self.conn.commit()
            if sql_upper.startswith('INSERT'):
                lastrowid = cursor.lastrowid
                cursor.close()
                return lastrowid
            else:
                cursor.close()
                return None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()