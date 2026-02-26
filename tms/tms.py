import json

import tms.tester as tst
import tms.scenario as scn

class TMS:
    def __init__(self):
        self.testers: list['tst.Tester'] = []
        self.scenarios: list['scn.Scenario'] = []

    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'type': 'TMS',
            'testers': list(map(lambda x: x.to_dict(), self.testers)),
            'scenarios': list(map(lambda x: x.to_dict(), self.scenarios))
        }

    def add_tester(self, name: str, level: int):
        '''Добавление нового тестировщика в систему.'''
        if self.__is_tester_exists(name):
            raise Exception(f'{name} alreade exists.')
        else:
            tester = tst.Tester(self, name, level)
            self.testers.append(tester)


    def __is_tester_exists(self, tester_name) -> bool:
        for tester in self.testers:
            if tester.name == tester_name:
                return True
        return False

    def get_tester(self, tester_name: str):
        '''Получение тестировщика по имени.'''
        for tester in self.testers:
            if tester.name == tester_name:
                return tester
        raise Exception(f'{tester_name} not found in tms.')

    def remove_tester(self, tester_name: str):
        '''Удаление тестировщика по имени.'''
        for tester in self.testers:
            if tester.name == tester_name:
                self.testers.remove(tester)
                return
        raise Exception(f'{tester_name} not found in tms.')

    def rename_tester(self, old_name: str, new_name: str):
        '''Переименование тестировщика.'''
        tester = self.get_tester(old_name)
        tester.name = new_name