from tms.tms import TestManagmentSystem
from tms.tester import Tester
from tms.scenario import Scenario
from tms.step import Step
from tms.bug import Bug

tms = TestManagmentSystem()

kirill = tms.add_tester('Kirill', 1)

kirill.create_scenario('проверка авторизации')

print(f'{tms}')