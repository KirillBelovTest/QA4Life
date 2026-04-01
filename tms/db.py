import sqlite3
import tms.models as models
from typing import Any, Literal

class TMSDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        models.Tester.create_table(self)
        models.Bug.create_table(self)

    def execute(self, query: str, params: tuple = ()):
        '''Выполняет запрос каждый раз создавая новое соединение.'''
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

        finally:
            cursor.close()
            conn.close()

    def insert(self, query: str, params: tuple = ()) -> int:
        '''Выполняет запрос каждый раз создавая новое соединение.'''
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            id = cursor.lastrowid
            if isinstance(id, int):
                return id
            else:
                raise Exception('Insert failed.')

        finally:
            cursor.close()
            conn.close()

    def select_one(self, query: str, params: tuple = ()) -> int:
        '''Выполняет запрос каждый раз создавая новое соединение.'''
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            one = cursor.fetchone()
            if isinstance(one, tuple):
                return dict(one)
            else:
                raise Exception('Insert failed.')

        finally:
            cursor.close()
            conn.close()
