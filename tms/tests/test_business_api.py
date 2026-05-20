import os
from typing import Any, Optional

from pytest import raises
from pytest import mark
from pytest import fixture
import requests

DEFAULT_PORT = 8000
DEFAULT_URL = f'http://localhost:{DEFAULT_PORT}'
DB_PATH = "tms.db"


class Tester:
    def __init__(self, id: int, name: str, grade: int):
        self.id = id
        self.name = name
        self.grade = grade

    @staticmethod
    def from_dict(data: dict[str, Any]):
        return Tester(data['id'], data['name'], data['grade'])

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'grade': self.grade}


class Bug:
    def __init__(self, id: int, title: str, status: str, author_id: int):
        self.id = id
        self.title = title
        self.status = status
        self.author_id = author_id

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Bug:
        return Bug(data['id'], data['title'], data['status'], data['author_id'])

    def to_dict(self) -> dict:
        return {'id': self.id, 'title': self.title, 'status': self.status, 'author_id': self.author_id}


class TMSClient:
    def __init__(self, url: str):
        self.url = url

    def create_tester(self, name: str, grade: int) -> Tester:
        tester_id = requests.post(f'{self.url}/testers', json={'name': name, 'grade': grade}).json()
        response = requests.get(f'{self.url}/testers?id={tester_id}')
        data = response.json()
        print(data)
        return Tester.from_dict(data)

    def get_tester(self, tester: Tester) -> Tester:
        response = requests.get(f'{self.url}/testers?id={tester.id}')
        data = response.json()
        return Tester.from_dict(data)

    def promote_tester(self, tester: Tester, new_grade: int):
        requests.put(f'{self.url}/testers/{tester.id}?grade={new_grade}')

    def create_bug(self, title: str, author_id: int) -> Bug:
        raise NotImplemented()

    def get_bug(self, tester: Tester) -> Tester:
        raise NotImplemented()

    def close_bug(self, bug: Tester):
        raise NotImplemented()

    def reopen_bug(self, bug: Bug):
        raise NotImplemented()


@fixture(scope='session', autouse=True)
def clean_database():
    """Пересоздаем базу перед каждым тестом"""
    # Удаляем файл базы
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    # Создаем новую (инициализация произойдет при первом запросе)
    yield


@fixture(scope='function')
def tms_client():
    # Создаем клиент перед каждым тестом
    client = TMSClient(DEFAULT_URL)
    yield client

@mark.client
@mark.parametrize('name,grade', [('kirill', 1), ('eugeny', 2), ('gleb', 4)])
def test_create_tester(tms_client: TMSClient, name: str, grade: int):
    tester = tms_client.create_tester(name, grade)
    assert tester.name == name
    assert tester.grade == grade

@mark.client
@mark.parametrize('name,grade,new_grade', [('dima', 1, 2), ('petr', 2, 3), ('grisha', 4, 5)])
def test_promote_tester(tms_client: TMSClient, name: str, grade: int, new_grade: int):
    tester = tms_client.create_tester(name, grade)
    tms_client.promote_tester(tester, new_grade)
    promoted_tester = tms_client.get_tester(tester)
    assert promoted_tester.name == name
    assert promoted_tester.grade == new_grade