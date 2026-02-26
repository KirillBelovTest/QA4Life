import json
import tms.step as stp
import tms.tester as tst

class Scenario:
    def __init__(self, author: 'tst.Tester', name: str):
        self.name = name
        self.author: 'tst.Tester' = author
        self.steps: list['stp.Step'] = []

    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'type': 'Scenario',
            'name': self.name,
            'author': self.tester.name,
            'steps': list(map(lambda x: x.to_dict(), self.steps))
        }
