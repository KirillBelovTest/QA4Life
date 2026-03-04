import json

import tms.tms as tms
import tms.scenario as scn
import tms.bug as bg

class Tester:
    def __init__(self, tms: 'tms.TMS', name: str, level: int):
        self.tms = tms
        self.name = name
        self.level = level
        self.current_scenario: 'scn.Scenario' = None
    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'type': 'Tester',
            'name': self.name,
            'level': self.level,
            'current_scenario': self.current_scenario.name if isinstance(self.current_scenario, scn.Scenario) else ''
        }

    def create_scenario(self, scenario_name: str):
        '''Тестировщик создает новый сценарий.'''
        scenario = scn.Scenario(self, scenario_name)
        self.tms.scenarios.append(scenario)

    def remove_scenario(self, scenario_name: str):
        '''Тестировщик удаляет существующий сценарий.'''
        for scenario in self.tms.scenarios:
            if scenario.name == scenario_name:
                self.tms.scenarios.remove(scenario)

    def take_scenario(self, scenario_name: str):
        '''Тестировщик берет сценарий в работу.'''
        for scenario in self.tms.scenarios:
            if scenario.name == scenario_name:
                self.current_scenario = self.tms.get_scenario(scenario_name)
                self.current_step_number = 0
                return
        raise Exception(f'{scenario_name} not found in tms scenarios.')

    def add_step(self, name: str, expected: str):
        '''Тестировщик шаг в текущий рабочий сценарий.'''
        step = (name, expected)
        self.current_scenario.steps.append(step)

    def create_bug(self, title: str, steps_to_reproduce: list[str]):
        '''Тестировщик создаёт ошибку на текущем шаге.'''
        bug = bg.Bug(self.current_scenario, title, steps_to_reproduce)
        self.current_scenario.bugs.append(bug)
        return bug

    def change_bug_status(self, bug_index: int, new_status: str):
        '''Тестировщик меняет статус ошибки.'''
        if bug_index < 0 or bug_index >= len(self.current_step.bugs):
            raise Exception(f'Bug with index {bug_index} not found.')

        valid_statuses = ['open', 'closed', 'in_progress', 'wont_fix']
        if new_status not in valid_statuses:
            raise Exception(f'Invalid status. Must be one of: {valid_statuses}')

        self.current_step.bugs[bug_index].status = new_status