from .tester import Tester
from .scenario import Scenario

class TestManagmentSystem:
    def __init__(self):
        self.testers = []
        self.scenarios = []

    def __repr__(self):
        return f'''{{\n\ttesters: {self.testers}, \n\tscenarios: {self.scenarios}}}'''

    def add_tester(self, name: str, level: int):
        tester = Tester(self, name, level)
        self.testers.append(tester)

    def get_tester(self, tester_name: str) -> 'Tester':
        return filter(lambda t: t.name == tester_name, self.testers)[0]

    def get_scenario(self, scenario_name: str) -> 'Scenario':
        return filter(lambda s: s.name == scenario_name, self.scenarios)
