from .step import Step
from .tester import Tester

class Scenario:
    def __init__(self, tester: 'Tester', name: str):
        self.name = name
        self.tester = tester
        self.steps = []

    def add_step(self, step_name: str, expected_result: str):
        step = Step(self, step_name, expected_result)
        self.steps.append(step)

    def __repr__(self):
        return f'Scenario(name = {self.name}, steps = {self.steps})'