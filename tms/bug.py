import tms.scenario as scn
import tms.step as stp

class Bug:
    def __init__(self, scenario: scn.Scenario, steps_to_reproduce: list[stp.Step]):
        self.scenario = scenario
        self.steps_to_reproduce = steps_to_reproduce
        self.status = 'open'