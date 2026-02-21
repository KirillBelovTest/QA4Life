import tms.tester as tst
import tms.scenario as scn

class TestManagmentSystem:
    def __init__(self):
        self.testers = []
        self.scenarios = []

    def __repr__(self):
        testers: str = '[\n'
        for tester in self.testers:
            testers += f'    {tester}\n'
        testers += '  ]'

        scenarios: str = '[\n'
        for scenario in self.scenarios:
            scenarios += f'.   {scenario}\n'
        scenarios += '  ]'

        return f'''TestManagmentSystem(\n  testers: {testers}, \n  scenarios: {scenarios}\n)'''

    def add_tester(self, name: str, level: int):
        tester = tst.Tester(self, name, level)
        self.testers.append(tester)

    def get_scenario(self, scenario_name: str) -> scn.Scenario:
        for s in self.scenarios:
            scenario: scn.Scenario = s
            if scenario.name == scenario_name:
                return scenario
        raise Exception(f'scenario {scenario_name} not found in tms.')