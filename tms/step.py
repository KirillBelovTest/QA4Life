from .scenario import Scenario

class Step:
    def __init__(self, scenario: Scenario, step_name: str, expected_result: str):
        self.scenario = scenario
        self.name = step_name
        self.expected_result = expected_result
        self.bugs = []

    def __repr__(self):
        return f'\n\t\tStep({self.name}, expected_result = {self.expected_result})'

    def execute(self, actual_result: str) -> bool:
        return self.expected_result == actual_result