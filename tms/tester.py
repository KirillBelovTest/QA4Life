from .tms import TestManagmentSystem
from .scenario import Scenario
from .step import Step

class Tester:
    def __init__(self, tms: 'TestManagmentSystem', name: str, level: int):
        self.tms: TestManagmentSystem = tms
        self.name: str = name
        self.level: int = level
        self.current_scenario: Scenario

    def __repr__(self):
        return f'{{name: {self.name}, level: {self.level}}}'

    def create_scenario(self, scenario_name: str):
        scenario = Scenario(self, scenario_name)
        self.current_scenario = scenario
        self.tms.scenarios.append(scenario)

    def take_scenario(self, scenario_name: str):
        self.current_scenario = self.tms.get_scenario(scenario_name)

    def add_step(self, name: str, expected: str):
        self.current_scenario.steps.append(Step(self.current_scenario, name, expected))

    def take_next_step(self):
        scenario: 'Scenario' = self.current_scenario
        self.current_step = scenario.next_step()

    def execute_step(self, actual: str) -> 'bool':
        return self.current_step.execute(actual)