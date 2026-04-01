import sqlite3
import tms.tms as tms
from typing import Any, Literal

class TMSDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        tms.Tester.create_table(self)
        tms.Bug.create_table(self)

    def execute(self,
                query: str,
                params: tuple = (),
                fetch: Literal['all', 'one', 'id', None] = None) -> None | int | 'dict[str, Any]' | 'list[dict[str, Any]]':
        '''Выполняет запрос каждый раз создавая новое соединение.'''
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
