from pytest import raises
from pytest import mark
from pytest import fixture
import requests

class TMSClient:
    def __init__(self, host: str = 'localhost', port: int = 8000):
        self.host: str = host
        self.port: int = port

    def build_url(self, method: str):
        return f'http://{self.host}:{self.port}/api/{method}'

    def get_tms(self):
        url = f'{self.base_url}/api/tms'
        response = requests.get(url)
        return response.json()

DEFAULT_PORT = 8000

@mark.api
def test_get_tms():
    tms_client = TMSClient('localhost', DEFAULT_PORT)
    tms_dict = tms_client.get_tms()
    assert tms_dict['testers'] == []