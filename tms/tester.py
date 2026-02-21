from .tms import TestManagmentSystem
from .scenario import Scenario
from .step import Step

class Tester:
    def __init__(self, tms: 'TestManagmentSystem', name: str, level: int):
        self.tms = tms
        self.name = name
        self.level = level
        self.current_scenario

    def __repr__(self):
        return f'{{name: {self._name}, level: {self._level}}}'

    def create_scenario(self, scenario_name: str):
        scenario = Scenario(self, scenario_name)
        self.current_scenario = scenario
        self.tms.scenarios.append(scenario)

    def take_scenario(self, scenario_name: str):
        self.current_scenario = self._tms.get_scenario_by_name(scenario_name)

    def add_step(self, name: str, expected: str):
        self.current_scenario.steps.append(Step(self.current_scenario, name, expected))

    def take_next_step(self):
        scenario = self.current_scenario
        self.current_step = scenario.next_step()

    def execute_step(self, actual: str) -> 'bool':
        return self.current_step.execute(actual)