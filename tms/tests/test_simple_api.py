import os

from pytest import raises
from pytest import mark
from pytest import fixture
import requests

DEFAULT_PORT = 8000
DEFAULT_URL = f'http://localhost:{DEFAULT_PORT}'
DB_PATH = "tms.db"


@fixture(scope='session', autouse=True)
def clean_database():
    """Пересоздаем базу перед каждым тестом"""
    # Удаляем файл базы
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    # Создаем новую (инициализация произойдет при первом запросе)
    yield


@mark.api
@mark.parametrize('name,grade', [('kirill', 1), ('eugeny', 2), ('gleb', 4)])
def test_get_create_tester(name: str, grade: int):
    # Создаем тестировщика, получаем id
    tester_id = requests.post(f'{DEFAULT_URL}/testers', json={'name': name, 'grade': grade}).json()

    # Получаем тестировщика по id
    tester = requests.get(f'{DEFAULT_URL}/testers?id={tester_id}').json()

    # Проверяем что созданный тестировщик имеет правильные поля
    assert tester['id'] == tester_id
    assert tester['name'] == name
    assert tester['grade'] == grade


@mark.api
@mark.parametrize('name,grade', [('ivan', -1), ('oleg', 3), ('viktor', 5)])
def test_update_tester_grade(name: str, grade: int):
    # Создаем тестировщика
    tester_id = requests.post(f'{DEFAULT_URL}/testers', json={'name': name, 'grade': grade}).json()

    new_grade = grade + 1

    # Обновляем уровень
    response = requests.put(f'{DEFAULT_URL}/testers/{tester_id}?grade={new_grade}')
    updated_tester = response.json()

    assert updated_tester['name'] == name
    assert updated_tester['grade'] == new_grade
    assert updated_tester['id'] == tester_id


@mark.api
def test_create_bug_form_urlencoded():
    # Создаем тестировщика
    tester_id = requests.post(f'{DEFAULT_URL}/testers', json={'name': 'maria', 'grade': 2}).json()

    # Создаем баг через form data
    response = requests.post(
        f'{DEFAULT_URL}/bugs?author_id={tester_id}',
        data={'title': 'login failed', 'status': 'opened'}
    )
    bug_id = response.json()
    assert isinstance(bug_id, int)

    # Получаем созданный баг по id
    bug = requests.get(f'{DEFAULT_URL}/bugs?id={bug_id}').json()

    # Проверяем что баг создан правильно
    assert bug['id'] == bug_id
    assert bug['title'] == 'login failed'
    assert bug['status'] == 'opened'
    assert bug['author_id'] == tester_id


@mark.api
def test_update_bug_status_text_plain():
    # Создаем тестировщика
    tester_id = requests.post(f'{DEFAULT_URL}/testers', json={'name': 'ivan', 'grade': 1}).json()

    # Создаем баг
    bug_id = requests.post(
        f'{DEFAULT_URL}/bugs?author_id={tester_id}',
        data={'title': 'crash on start', 'status': 'opened'}
    ).json()

    # Обновляем статус через text/plain
    response = requests.put(
        f'{DEFAULT_URL}/bugs/{bug_id}?field=status',
        data='closed',
        headers={'Content-Type': 'text/plain'}
    )

    assert response.status_code == 200
    assert 'closed' in response.text

    # Получаем баг и проверяем что статус обновился
    bug = requests.get(f'{DEFAULT_URL}/bugs?id={bug_id}').json()
    assert bug['status'] == 'closed'


@mark.api
def test_get_bugs_with_filter():
    # Создаем тестировщика
    tester_id = requests.post(f'{DEFAULT_URL}/testers', json={'name': 'olga', 'grade': 3}).json()

    # Создаем несколько багов
    bug1_id = requests.post(f'{DEFAULT_URL}/bugs?author_id={tester_id}',
                            data={'title': 'bug1', 'status': 'opened'}).json()
    bug2_id = requests.post(f'{DEFAULT_URL}/bugs?author_id={tester_id}',
                            data={'title': 'bug2', 'status': 'closed'}).json()

    # Фильтруем по статусу (GET /bugs?status=closed)
    closed_bugs = requests.get(f'{DEFAULT_URL}/bugs?status=closed').json()

    # Проверяем что в ответе только закрытые баги
    assert isinstance(closed_bugs, list)
    assert len(closed_bugs) >= 1
    assert all(bug['status'] == 'closed' for bug in closed_bugs)

    # Проверяем что наш закрытый баг есть в списке
    closed_bug_ids = [bug['id'] for bug in closed_bugs]
    assert bug2_id in closed_bug_ids


@mark.api
def test_get_testers_with_filter():
    # Создаем тестировщиков с разными уровнями
    tester1_id = requests.post(f'{DEFAULT_URL}/testers', json={'name': 'john', 'grade': 1}).json()
    tester2_id = requests.post(f'{DEFAULT_URL}/testers', json={'name': 'jane', 'grade': 2}).json()
    tester3_id = requests.post(f'{DEFAULT_URL}/testers', json={'name': 'jim', 'grade': 1}).json()

    # Фильтруем по уровню (grade передается как int в запросе)
    grade1_testers = requests.get(f'{DEFAULT_URL}/testers?grade=1').json()

    # Проверяем что все тестировщики имеют grade=1
    assert isinstance(grade1_testers, list)
    assert len(grade1_testers) >= 2
    assert all(tester['grade'] == 1 for tester in grade1_testers)

    # Проверяем что наши тестировщики с grade=1 есть в списке
    grade1_tester_ids = [tester['id'] for tester in grade1_testers]
    assert tester1_id in grade1_tester_ids
    assert tester3_id in grade1_tester_ids

    # Проверяем что тестировщик с grade=2 не попал в фильтр
    assert tester2_id not in grade1_tester_ids