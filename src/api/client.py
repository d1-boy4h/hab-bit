import json
from os import sep
from ..models import Day, Task

class Client:
    '''Класс для работы с JSON - сохранение и загрузка данных.'''
    def __init__(
        self,
        logger=None,
        data_folder='data',
        tasks_filename='tasks_data.json',
        days_filename='days_data.json'
    ):
        self._tasks_data_filename = data_folder + sep + tasks_filename
        self._days_data_filename = data_folder + sep + days_filename

        self._logger = logger # TODO: Реализовать логгер

    def _fetch(self, filename, fetching_class):
        '''Загрузка данных их JSON.'''
        try:
            with open(filename, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            # TODO: Вставить тут логер с предупреждением
            # raise Warning(f'{filename}: файл не найден')
            return list()

        return [fetching_class(**elem) for elem in data]

    def fetch_tasks(self):
        '''Загрузка задач из JSON.'''
        return self._fetch(self._tasks_data_filename, Task)

    def fetch_days(self):
        '''Загрузка дней из JSON.'''
        return self._fetch(self._days_data_filename, Day)

    def _dump(self, filename, data_list):
        '''Сохранение данных в JSON.'''
        dump_data = [elem.to_dict() for elem in data_list]

        try:
            with open(filename, 'w', encoding='utf-8') as json_file:
                json.dump(dump_data, json_file, ensure_ascii=False, indent=2)
        except json.JSONDecodeError:
            # TODO: Вставить тут логер с ошибкой
            # raise Error(f'{filename}: файл не найден')
            pass

    def dump_tasks(self, tasks):
        '''Сохранение задач в JSON.'''
        return self._dump(self._tasks_data_filename, tasks)

    def dump_days(self, days):
        '''Сохранение дней в JSON.'''
        return self._dump(self._days_data_filename, days)
