import pytest
from tms.tms import TMS

@pytest.fixture(scope='module')
def created_tms():
    new_tms = TMS()
    yield new_tms
#   вот тут могут быть какие-то действия после всех и любых тестов

@pytest.fixture(scope='module')
def tms(created_tms):
    created_tms.add_tester('kirill', 1)
    created_tms.add_tester('eugeny', 2)
    yield created_tms

def test_create_tester(tms):
    assert tms.get_tester('kirill').name == 'kirill'

def test_remove_tester(tms):
    before_testers_count = len(tms.testers)
    tms.remove_tester('kirill')
    after_testers_count = len(tms.testers)
    assert after_testers_count == before_testers_count - 1

def test_rename_tester(tms):
    tms.rename_tester('kirill', 'eugeny')
    assert tms.get_tester('eugeny').name == 'eugeny'

def test_tester_not_found(tms):
    with pytest.raises(Exception) as ex:
        tms.get_tester('any_name')

    assert ex.value.args[0] == 'any_name not found in tms.'

def test_cant_add_tester(tms: TMS):
    tester_name = 'unique_tester_name'
    tms.add_tester(tester_name, 1)
    with pytest.raises(Exception):
        tms.add_tester(tester_name, 1)