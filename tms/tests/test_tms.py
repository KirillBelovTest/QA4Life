from pytest import raises
from pytest import fixture
from tms.tms import TMS

@fixture(scope='module')
def tms():
    new_tms = TMS()
    yield new_tms

def test_create_tester(tms: TMS):
    berfore_testers_count = len(tms.testers)
    tester_name = 'new_tester1'
    tms.add_tester(tester_name, 1)
    tester = tms.get_tester(tester_name)
    after_tester_count = len(tms.testers)
    assert tester.name == tester_name
    assert berfore_testers_count + 1 == after_tester_count

def test_remove_tester(tms):
    tester_name = 'tester_for_remove'
    tms.add_tester(tester_name, 1)
    before_testers_count = len(tms.testers)
    tms.remove_tester(tester_name)
    after_testers_count = len(tms.testers)
    assert after_testers_count == before_testers_count - 1

def test_rename_tester(tms):
    old_tester_name = 'kirill'
    new_tester_name = 'eugeny'
    tms.add_tester(old_tester_name, 1)
    tms.rename_tester(old_tester_name, new_tester_name)
    tester = tms.get_tester(new_tester_name)
    assert tester.name == new_tester_name

def test_tester_not_found(tms):
    with raises(Exception) as ex:
        tms.get_tester('any_name')
    assert ex.value.args[0] == 'any_name not found in tms.testers.'

def test_cant_add_tester(tms: TMS):
    tester_name = 'unique_tester_name'
    tms.add_tester(tester_name, 1)
    with raises(Exception):
        tms.add_tester(tester_name, 1)