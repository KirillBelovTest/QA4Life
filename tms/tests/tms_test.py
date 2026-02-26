from tms.tms import TMS

def test_create_tester():
    tms = TMS()
    tms.add_tester('kirill', 1)
    assert tms.get_tester('kirill').name == 'kirill'