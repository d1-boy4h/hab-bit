import json
from os import sep
from typing import Any, Dict, List
from pathlib import Path

class Database:
    '''
    Имитация подключения к БД. На данный момент работает с JSON для сохранения и загрузки данных.
    '''
    def __init__(self, data_folder: str = 'data'):
        self._data_folder = data_folder
        self._ensure_data_folder()

    def _ensure_data_folder(self):
        '''Создаёт папку для данных, если её нет.'''
        Path(self._data_folder).mkdir(exist_ok=True)

    def _get_file_path(self, filename: str) -> str:
        '''Возвращает полный путь к файлу.'''
        return self._data_folder + sep + filename

    def read_table(self, table_name: str) -> List[Dict[str, Any]]:
        '''Читает всю таблицу (аналог SELECT * FROM table).'''
        file_path = self._get_file_path(f'{table_name}.json')

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def write_table(self, table_name: str, data: List[Dict[str, Any]]):
        '''Записывает таблицу (аналог TRUNCATE + INSERT).'''
        file_path = self._get_file_path(f'{table_name}.json')

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
