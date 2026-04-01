import sqlite3
from typing import Any, Literal

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


    def execute(self,
                query: str,
                params: tuple = (),
                fetch: Literal['all', 'one', 'id', None] = None) -> None | int | 'dict[str, Any]' | 'list[dict[str, Any]]':
        """Execute query with new connection"""
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
