from tms.tms import ManagmentSystem

def test_create_scenario():
    tms = ManagmentSystem()
    tms.add_tester('kirill', 1)
    assert tms.get_tester('kirill').name == 'kirill'