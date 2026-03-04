import json

import tms.scenario as scn

class Bug:
    def __init__(self, scenario_name: str, title: str, steps_to_reproduce: list[(str, str)]):
        self.scenario_name = scenario_name
        self.title = title
        self.steps_to_reproduce = steps_to_reproduce
        self.status = 'open'

    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'type': 'Bug',
            'description': self.title,
            'scenario': self.scenario_name,
            'status': self.status,
            'steps_to_reproduce': self.steps_to_reproduce
        }