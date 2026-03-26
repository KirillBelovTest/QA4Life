class Tester:
    table_name: str = 'testers'

    def __init__(self, name: str, level: int):
        self.id = None
        self.name = name
        self.level = level

    @staticmethod
    def create_table() -> str:
        return f"""
        CREATE TABLE IF NOT EXISTS {Tester.table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            level INTEGER NOT NULL
        )
        """

    @staticmethod
    def get_from_table(name: str) -> str:
        return f"SELECT * FROM {Tester.table_name} WHERE name = '{name}'"

    def insert_into_table(self) -> str:
        return f"""
        INSERT INTO {Tester.table_name} (name, level)
        VALUES ('{self.name}', '{self.level}')
        """

    def delete_from_table(self) -> str:
        if self.id is None:
            raise ValueError("Tester not inserted yet")
        return f"DELETE FROM {Tester.table_name} WHERE id = {self.id}"

    def update_in_table(self) -> str:
        if self.id is None:
            raise ValueError("Tester not inserted yet")
        return f"""
        UPDATE {Tester.table_name}
        SET name = '{self.name}', level = '{self.level}'
        WHERE id = {self.id}
        """

    def to_dict(self):
        return {
            'type': 'Tester',
            'id': self.id,
            'name': self.name,
            'level': self.level
        }

    @staticmethod
    def from_dict(data: 'dict[str, str|int]') -> 'Tester':
        return Tester(str(data['name']), int(data['level']))