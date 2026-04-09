import sqlite3
import tms.models as models
from typing import Any, Literal, Optional

class TMSDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        models.Tester.create_table(self)
        models.Bug.create_table(self)

    def execute(self, query: str, params: tuple = (), fetch: Literal['all', 'one', 'id', None] = None):
        '''Выполняет запрос каждый раз создавая новое соединение.'''
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

            match fetch:
                case 'all':
                    return cursor.fetchall()
                case 'one':
                    return cursor.fetchone()
                case 'id':
                    return cursor.lastrowid

        finally:
            cursor.close()
            conn.close()

    def save(self, table: str, id: Optional[int], values: dict[str, Any]):
        if id:
            set_values = []
            for k in values:
                if isinstance(values[k], int):
                    set_values.append(f'{k} = {values[k]}')
                else:
                    set_values.append(f"{k} = '{values[k]}'")
            set_values_str = ', '.join(set_values)
            query = f'''
                UPDATE {table}
                SET
                    {set_values_str}
                WHERE
                    id = {id};
            '''
            print(query)
            self.execute(query=query)
            return id
        else:
            cols = []
            vals = []
            for k in values:
                cols.append(f'{k}')
                vals.append(f"'{values[k]}'")
            cols_str = ','.join(cols)
            vals_str = ','.join(vals)
            query = f'''
                INSERT INTO {table} ({cols_str})
                VALUES ({vals_str});
            '''
            return self.execute(query=query, fetch='id')


    def get_from_table(self, table: str, id: Optional[int], filters: dict[str, Any]):
        if id:
            query = f'''
                SELECT * FROM {table} WHERE id = {id}
            '''

            result = self.execute(query=query, fetch='one')
            return dict(result)

        query = f'''
            SELECT * FROM {table}
        '''

        where = []

        for k in filters:
            if filters[k]:
                where.append(f"{k} = '{filters[k]}'")

        if len(where) > 0:
            query += ' WHERE '
            query += ' AND '.join(where)

        query += ';'

        result = self.execute(query=query, fetch='all')
        return list(map(lambda x: dict(x), result))
