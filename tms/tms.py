from typing import Optional

from pydantic import BaseModel

from tms.db import SQLiteDatabase


class Tester(BaseModel):
    id: Optional[int] = None
    name: str
    grade: int

    def save(self, db: SQLiteDatabase, table: str):
        query = f'''
            INSERT INTO {table} (name, grade)
            VALUES ({self.name}, {self,self.grade});
        '''
        self.id = db.execute(query=query, fetch='id')