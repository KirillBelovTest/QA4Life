from typing import Any

import tms.tester as tst
import tms.scenario as scn

class ManagmentSystem:
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
            scenarios += f'    {scenario}\n'
        scenarios += '  ]'

        return f'''ManagmentSystem(\n  testers: {testers}, \n  scenarios: {scenarios}\n)'''

    def add_tester(self, name: str, level: int):
        '''Добавление нового тестировщика в систему.'''
        tester = tst.Tester(self, name, level)
        self.testers.append(tester)

    def get_tester(self, tester_name: str) -> 'tst.Tester':
        '''Получение тестировщика по имени.'''
        return self.__find_first_by_name(self.testers, tester_name)

    def get_scenario(self, scenario_name: str) -> 'scn.Scenario':
        '''Получение сценария по названию.'''
        return self.__find_first_by_name(self.scenarios, scenario_name)

    def __find_first_by_name(_, collection: list[Any], name: str) -> Any:
        for item in collection:
            if item.name == name:
                return item
        raise Exception(f'{name} not found in collection.')