import tms.tms as tms
import tms.scenario as scn
import tms.step as stp

class Tester:
    def __init__(self, tms: 'tms.ManagmentSystem', name: str, level: int):
        self.tms = tms
        self.name = name
        self.level = level

    def __repr__(self):
        return f'Tester(name = {self.name}, level = {self.level})'

    def create_scenario(self, scenario_name: str):
        '''Тестировщик создает сценарий и
        результат автоматически добавляется
        в общий список сценариев системы.'''
        scenario = scn.Scenario(self, scenario_name)
        self.tms.scenarios.append(scenario)

    def take_scenario(self, scenario_name: str):
        '''Тестировщик берет задачу
        на выполнение или обновление сценария.'''
        self.current_scenario = self.tms.get_scenario(scenario_name)
        self.current_step_number = 0

    def add_step(self, name: str, expected: str):
        '''Тестировщик может добавить в сценарий шаг и ожидаемый результат.'''
        step = stp.Step(self.current_scenario, name, expected)
        step_number = self.current_step_number + 1
        self.current_scenario.steps.insert(step_number, step)

    def take_next_step(self):
        '''Тестировщик может перейти к следующему шагу
        и если шаги заканчиваются, то текущий шаг,
        над которым работает тестироващик принимает
        значение None.'''
        self.current_step_number += 1
        self.current_step = self.create_scenario

    def execute_step(self, actual_result: str) -> 'bool':
        '''Тестировщик выполняет текущий шаг и указывает
        фактический результат.'''
        if self.current_step_number >= 0 and self.current_step_number < len(self.current_scenario.steps):
            expected_result = self.current_scenario.steps[self.current_step_number].expected_result
            return expected_result == actual_result
        raise Exception(f'Step {self.current_step_number} out of range.')