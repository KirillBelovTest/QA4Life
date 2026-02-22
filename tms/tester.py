import tms.tms as tms
import tms.scenario as scn
import tms.step as stp

class Tester:
    def __init__(self, tms: tms.TestManagmentSystem, name: str, level: int):
        self.tms = tms
        self.name = name
        self.level = level

    def __repr__(self):
        return f'Tester(name = {self.name}, level = {self.level})'

    def create_scenario(self, scenario_name: str):
        scenario = scn.Scenario(self, scenario_name)
        self.current_scenario = scenario
        self.tms.scenarios.append(scenario)

    def take_scenario(self, scenario_name: str):
        self.current_scenario = self.tms.get_scenario(scenario_name)

    def add_step(self, name: str, expected: str):
        self.current_scenario.steps.append(stp.Step(self.current_scenario, name, expected))

    def take_next_step(self):
        scenario = self.current_scenario
        step = scenario.get_next_step()
        self.current_step = step

    def execute_step(self, actual: str) -> 'bool':
        if self.current_step != None:
            return self.current_step.execute(actual)
        return False