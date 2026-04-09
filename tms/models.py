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
            );
        ''')

    def save(self, db: db.TMSDatabase):
        self.id = db.save(Tester.TABLE, self.id, {'name': self.name, 'grade': self.grade})

    @staticmethod
    def get_from_table(db: db.TMSDatabase,
                       id: Optional[int] = None,
                       name: Optional[str] = None,
                       grade: Optional[int] = None):
        result = db.get_from_table(Tester.TABLE, id,
                                   {'name': name, 'grade': grade})
        if isinstance(result, dict):
            return Tester(**result)
        return list(map(lambda t: Tester(**dict(t)), result))

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
        self.id = db.save(Bug.TABLE, self.id,
                {'title': self.title, 'status': self.status, 'author_id': self.author_id})

    @staticmethod
    def get_from_table(db: db.TMSDatabase,
                       id: Optional[int] = None,
                       title: Optional[str] = None,
                       status: Optional[str] = None,
                       author_id: Optional[int] = None):
        result = db.get_from_table(Bug.TABLE, id,
                                   {'title': title, 'status': status, 'author_id': author_id})
        if isinstance(result, dict):
            return Bug(**result)
        return list(map(lambda x: Bug(**x), result))
