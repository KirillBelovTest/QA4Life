from typing import ClassVar, Optional, Any
from pydantic import BaseModel
import tms.db as db


class Tester(BaseModel):
    id: Optional[int] = None
    name: str
    grade: int
    TABLE: ClassVar[str] = 'testers'

    @staticmethod
    def create_table(db: db.TMSDatabase, table: str = 'testers'):
        Tester.TABLE = table
        db.execute(f'''
            CREATE TABLE IF NOT EXISTS {Tester.TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                grade INTEGER NOT NULL
            )
        ''')

    def save(self, db: db.TMSDatabase):
        if isinstance(self.id, int):
            query = f'''
                UPDATE {Tester.TABLE}
                SET
                    name = '{self.name}'
                    grade = {self.grade}
                WHERE
                    id = {self.id};
            '''
        else:
            query = f'''
                INSERT INTO {Tester.TABLE} (name, grade)
                VALUES ('{self.name}', '{self.grade}');
            '''
            id = db.execute(query=query, fetch='id')
            if id and isinstance(id, int):
                self.id = id

    @staticmethod
    def get_from_table(db: db.TMSDatabase,
                       id: Optional[int] = None,
                       name: Optional[str] = None,
                       grade: Optional[int] = None):
        if id:
            query = f'''
                SELECT * FROM {Tester.TABLE} WHERE id = {id}
            '''
            result = db.execute(query=query, fetch='one')
            if isinstance(result, dict):
                return Tester(**result)

        query = f'''
                SELECT * FROM {Tester.TABLE}
            '''

        where = []

        if name:
            where.append(f"name = '{name}'")

        if grade:
            where.append(f"grade = '{grade}'")

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
    def create_table(db: db.TMSDatabase, table: str = 'bugs'):
        Bug.TABLE = table
        db.execute(f'''
            CREATE TABLE IF NOT EXISTS {Bug.TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                status TEXT NOT NULL,
                author_id INTEGER NOT NULL,
                FOREIGN KEY (author_id) REFERENCES {Tester.TABLE} (id)
            )
        ''')

    def save(self, db: db.TMSDatabase):
        '''Сохраняет баг в БД.'''
        if self.id:
            query = f'''
                UPDATE
                    {Bug.TABLE}
                SET
                    title = '{self.title}',
                    status = '{self.status}',
                    author_id = '{self.author_id}'
                WHERE
                    id = {self.id}
            '''
            db.execute(query=query)
        else:
            query = f'''
                INSERT INTO {Bug.TABLE} (title, status, author_id)
                VALUES ('{self.title}', '{self.status}', {self.author_id});
            '''
            id = db.execute(query=query, fetch='id')
            if id and isinstance(id, int):
                self.id = id
                return id

    @staticmethod
    def get_from_table(db: db.TMSDatabase,
                       id: Optional[int] = None,
                       title: Optional[str] = None,
                       status: Optional[str] = None,
                       author_id: Optional[int] = None):
        if id:
            query = f'''
                SELECT * FROM {Bug.TABLE} WHERE id = {id}
            '''

            result = db.execute(query=query, fetch='one')
            print(result)
            if isinstance(result, dict):
                return Bug(**result)

        query = f'''
            SELECT * FROM {Bug.TABLE}
        '''

        where = []

        if title:
            where.append(f"title = '{title}'")
        if status:
            where.append(f"status = '{status}'")
        if author_id:
            where.append(f'author_id = {author_id}')

        if len(where) > 0:
            query += ' WHERE '
            query += ' AND '.join(where)

        query += ';'

        print(query)

        result = db.execute(query=query, fetch='all')
        if isinstance(result, list):
            return result
