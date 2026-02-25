import tms.step as stp
import tms.tester as tst

class Scenario:
    def __init__(self, tester: 'tst.Tester', name: str):
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