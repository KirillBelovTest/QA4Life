import json

import tms.scenario as scn
import tms.step as stp

class Bug:
    def __init__(self, scenario: 'scn.Scenario', steps_to_reproduce: list['stp.Step']):
        self.scenario = scenario
        self.steps_to_reproduce = steps_to_reproduce
        self.status = 'open'

    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'type': 'Bug',
            'scenario': self.scenario.name,
            'status': self.status,
            'steps_to_reproduce': list(map(lambda x: x.name, self.steps_to_reproduce))
        }