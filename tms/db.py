import sqlite3
from typing import Union, Literal

class TMSDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.execute("""
            CREATE TABLE IF NOT EXISTS testers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                grade TEXT NOT NULL
            )
        """)
        self.execute("""
            CREATE TABLE IF NOT EXISTS bugs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                steps TEXT,
                status TEXT DEFAULT 'open',
                tester_id INTEGER NOT NULL,
                attachments TEXT,
                FOREIGN KEY (tester_id) REFERENCES testers (id)
            )
        """)


    def execute(self, query: str, params: tuple = (), fetch: Literal['all', 'one', 'id', None] = None):
        """Execute query with current connection"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)

            if fetch == 'all':
                rows = cursor.fetchall()
                return [dict(row) for row in rows] if rows else []
            elif fetch == 'one':
                row = cursor.fetchone()
                return dict(row) if row else None
            elif fetch == 'id':
                conn.commit()
                return cursor.lastrowid
            else:  # None
                conn.commit()
                return None

        finally:
            cursor.close()
            conn.close()


    def create(self, table: str, **kwargs) -> int:
        """Insert record and return its ID"""
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['?' for _ in kwargs])
        values = tuple(kwargs.values())
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        return self.execute(query, values, fetch='id')


    def read(self, table: str, **kwargs) -> Union[dict, list, None]:
        """Select records. Returns single dict if 'id' provided, otherwise list"""
        if not kwargs:
            query = f"SELECT * FROM {table}"
            return self.execute(query, fetch='all')

        conditions = ' AND '.join([f"{k} = ?" for k in kwargs.keys()])
        values = tuple(kwargs.values())
        query = f"SELECT * FROM {table} WHERE {conditions}"

        if 'id' in kwargs:
            return self.execute(query, values, fetch='one')
        return self.execute(query, values, fetch='all')


    def update(self, table: str, item_id: int, **kwargs) -> bool:
        """Update record by ID"""
        if not kwargs:
            return False

        set_clause = ', '.join([f"{k} = ?" for k in kwargs.keys()])
        values = tuple(kwargs.values()) + (item_id,)
        query = f"UPDATE {table} SET {set_clause} WHERE id = ?"
        self.execute(query, values, fetch=None)
        return True


    def delete(self, table: str, item_id: int) -> bool:
        """Delete record by ID"""
        query = f"DELETE FROM {table} WHERE id = ?"
        self.execute(query, (item_id,), fetch=None)
        return True
