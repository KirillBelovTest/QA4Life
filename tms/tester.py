import json

import tms.tms as tms
import tms.scenario as scn
import tms.step as stp

class Tester:
    def __init__(self, tms: 'tms.TMS', name: str, level: int):
        self.tms = tms
        self.name = name
        self.level = level
        self.current_scenario: 'scn.Scenario'
        self.current_step: 'stp.Step'
        self.current_step_number: int = 0

    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'type': 'Tester',
            'name': self.name,
            'level': self.level,
            'current_scenario': self.current_scenario.name if isinstance(self.current_scenario, scn.Scenario) else '',
            'current_step': self.current_step.name if isinstance(self.current_step, stp.Step) else '',
            'current_step_number': self.current_step_number
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
        step = stp.Step(self.current_scenario, name, expected)
        step_number = self.current_step_number + 1
        self.current_scenario.steps.insert(step_number, step)

    def take_next_step(self):
        '''Тестировщик переходит к следующему шагу.'''
        self.current_step_number += 1
        self.current_step = self.current_scenario.steps[self.current_step_number - 1]

    def execute_step(self, actual_result: str) -> 'bool':
        '''Тестировщик выполняет текущий шаг и указывает фактический результат.'''
        if self.current_step_number >= 0 and self.current_step_number < len(self.current_scenario.steps):
            expected_result = self.current_scenario.steps[self.current_step_number].expected_result
            return expected_result == actual_result
        raise Exception(f'Step {self.current_step_number} out of range.')