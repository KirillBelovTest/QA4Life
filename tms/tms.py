from typing import ClassVar, Optional
from pydantic import BaseModel
from tms.db import TMSDatabase


class Tester(BaseModel):
    id: Optional[int] = None
    name: str
    grade: int
    TABLE: ClassVar[str] = None

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
        self.id = db.execute(query=query, fetch='id')

    @staticmethod
    def get_from_table(db: TMSDatabase, id: int = None, name: str = None, grade: int = None):
        if id:
            query = f'''
                SELECT * FROM {Tester.TABLE} WHERE id = {id}
            '''
            return db.execute(query=query, fetch='one')


class Bug(BaseModel):
    id: Optional[int] = None
    title: str
    status: str
    author_id: int
    TABLE: ClassVar[str] = None

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
                    author_id = {self.author}
                WHERE
                    id = {self.id}
            '''
        else:
            query = f'''
                INSERT INTO {Bug.TABLE} (title, status, author_id)
                VALUES ({self.title}, {self.status}, {self.author_id});
            '''
            self.id = db.execute(query=query, fetch='id')

    @staticmethod
    def get_from_table(db: TMSDatabase, id: int = None, title: str = None, status: str = None, author_id: int = None):
        if id:
            query = f'''
                SELECT * FROM {Tester.TABLE} WHERE id = {id}
            '''
            return db.execute(query=query, fetch='one')
