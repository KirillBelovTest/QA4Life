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


class TMSClient:
    def __init__(self, url: str):
        self.url = url

    def create_tester(self, name: str, grade: int) -> Tester:
        tester_id = requests.post(f'{self.url}/testers', json={'name': name, 'grade': grade})
        response = requests.get(f'{self.url}/testers?id={tester_id}')
        data = response.json()
        return Tester.from_dict(data)

    def get_tester(self, tester_id: int) -> Tester:
        response = requests.get(f'{self.url}/testers?id={tester_id}')
        data = response.json()
        return Tester.from_dict(data)

    def promote_tester(self, tester: Tester, new_grade: int):
        requests.put(f'{self.url}/testers/{tester.id}?grade={new_grade}')


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
    """Создаем клиент перед каждым тестом"""
    client = TMSClient(DEFAULT_URL)
    yield client


@mark.api
@mark.parametrize('name,grade', [('kirill', 1), ('eugeny', 2), ('gleb', 4)])
def test_create_tester(tms_client: TMSClient, name: str, grade: int):
    tester = tms_client.create_tester(name, grade)
    assert tester.name == name
    assert tester.grade == grade
