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

    def get_scenario(self, scenario_name: str) -> 'Scenario':
        for s in self.scenarios:
            scenario: Scenario = s
            if scenario.name == scenario_name:
                return scenario
        raise Exception(f'scenario {scenario_name} not found in tms.')