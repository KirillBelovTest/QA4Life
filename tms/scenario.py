import tms.step as stp
import tms.tester as tst

class Scenario:
    def __init__(self, tester: tst.Tester, name: str):
        self.name = name
        self.tester = tester
        self.steps: list[stp.Step] = []

    def __repr__(self):
        steps = f'Scenario(name = {self.name}, steps = '
        if len(self.steps) == 0:
            return steps + f'{self.steps})'
        steps += '[\n'
        for s in self.steps:
            steps += f'        {s}\n'
        steps += f'      ]\n    )'
        return steps

    def add_step(self, step_name: str, expected_result: str):
        step = stp.Step(self, step_name, expected_result)
        self.steps.append(step)

    def get_next_step(self) -> stp.Step | None:
        if not hasattr(self, 'current_step_number'):
            self.current_step_number = 0
        
        if self.current_step_number == len(self.steps):
            return None
        
        self.current_step_number += 1
        return self.steps[self.current_step_number - 1]