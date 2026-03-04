import json

import tms.tester as tst
import tms.bug as bg

class Scenario:
    def __init__(self, author: 'tst.Tester', name: str):
        self.name = name
        self.author: 'tst.Tester' = author
        self.steps: list[(str, str)] = []
        self.bugs: list['bg.Bug'] = []

    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'type': 'Scenario',
            'name': self.name,
            'author': self.author.name,
            'steps': self.steps,
            'bugs': self.bugs
        }
