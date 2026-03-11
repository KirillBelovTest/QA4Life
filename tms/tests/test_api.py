from pytest import raises
from pytest import mark
from pytest import fixture
import requests

@fixture
def api_client():
    client = requests.Session()
    yield client

@mark.api
def test_create_tester(api_client: requests.Session):
    response = api_client.get('http://localhost:8000/api/tms')
    assert response.status_code == 200