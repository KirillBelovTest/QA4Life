from typing import ClassVar, Optional, Any
from pydantic import BaseModel
from tms.db import TMSDatabase


class Tester(BaseModel):
    id: Optional[int] = None
    name: str
    grade: int
    TABLE: ClassVar[str] = 'testers'

    @staticmethod
    def create_table(db: TMSDatabase, table: str = 'testers'):
        Tester.TABLE = table
        db.execute(f"""
            CREATE TABLE IF NOT EXISTS {Tester.TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                grade TEXT NOT NULL
            )
        """)

    def save(self, db: TMSDatabase):
        query = f'''
            INSERT INTO {Tester.TABLE} (name, grade)
            VALUES ({self.name}, {self.grade});
        '''
        id = db.execute(query=query, fetch='id')
        if id and isinstance(id, int):
            self.id = id

    @staticmethod
    def get_from_table(db: TMSDatabase,
                       id: Optional[int] = None,
                       name: Optional[str] = None,
                       grade: Optional[int] = None):
        if id:
            query = f'''
                SELECT * FROM {Tester.TABLE} WHERE id = {id}
            '''
            result = db.execute(query=query, fetch='one')
            if isinstance(result, dict):
                Tester(**result)

        query = f'''
                SELECT * FROM {Tester.TABLE}
            '''

        where = []

        if name:
            where.append(f'name = {name}')

        if grade:
            where.append(f'grade = {grade}')

        if len(where) > 0:
            query += ' WHERE '
            query += ' AND '.join(where)

        result = db.execute(query=query, fetch='all')
        if isinstance(result, list):
            return list(map(lambda t: Tester(**t), result))

class Bug(BaseModel):
    id: Optional[int] = None
    title: str
    status: str
    author_id: int
    TABLE: ClassVar[str] = 'bugs'

    @staticmethod
    def create_table(db: TMSDatabase, table: str = 'bugs'):
        Bug.TABLE = table
        db.execute(f"""
            CREATE TABLE IF NOT EXISTS {Bug.TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                status TEXT NOT NULL,
                author_id INTEGER NOT NULL,
                FOREIGN KEY (author_id) REFERENCES {Tester.TABLE} (id)
            )
        """)

    def save(self, db: TMSDatabase):
        if self.id:
            query = f'''
                UPDATE
                    {Bug.TABLE}
                SET
                    title = {self.title},
                    status = {self.status},
                    author_id = {self.author_id}
                WHERE
                    id = {self.id}
            '''
        else:
            query = f'''
                INSERT INTO {Bug.TABLE} (title, status, author_id)
                VALUES ({self.title}, {self.status}, {self.author_id});
            '''
            id = db.execute(query=query, fetch='id')
            if id and isinstance(id, int):
                self.id = id

    @staticmethod
    def get_from_table(db: TMSDatabase,
                       id: Optional[int] = None,
                       title: Optional[str] = None,
                       status: Optional[str] = None,
                       author_id: Optional[int] = None):
        if id:
            query = f'''
                SELECT * FROM {Bug.TABLE} WHERE id = {id}
            '''

            result = db.execute(query=query, fetch='one')
            if isinstance(result, dict):
                return Bug(**result)

        query = f'''
            SELECT * FROM {Bug.TABLE}
        '''

        where = []

        if title:
            where.append(f'title = {title}')
        if status:
            where.append(f'status = {status}')
        if author_id:
            where.append(f'author_id = {author_id}')

        if len(where) > 0:
            query += ' WHERE '
            query += ' AND '.join(where)

        result = db.execute(query=query, fetch='all')
        if isinstance(result, list):
            return list(map(lambda b: Bug(**b)))
