import json

import tms.scenario as scn

class Step:
    def __init__(self, scenario: 'scn.Scenario', step_name: str, expected_result: str):
        self.scenario = scenario
        self.name = step_name
        self.expected_result = expected_result
        self.bugs = []

    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'type': 'Step',
            'name': self.name,
            'scenarion': self.scenario.name,
            'expected_result': self.expected_result,
            'bugs': list(map(lambda x: x.to_dict(), self.bugs))
        }