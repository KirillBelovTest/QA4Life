from pytest import raises
from pytest import mark
from pytest import fixture
import requests

DEFAULT_PORT = 8000
DEFAULT_URL = f'http://localhost:{DEFAULT_PORT}'

@mark.api
def test_get_create_tester():
    tester = requests.post(f'{DEFAULT_URL}/testers', json={'name':'kirill', 'grade':2}).json()
    testers = requests.get(f'{DEFAULT_URL}/testers').json()
    assert tester in testers