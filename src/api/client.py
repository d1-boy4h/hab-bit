from typing import List, Optional
from datetime import date as Date
import logging

from ..models import Task, Day
from ..server import Database, TasksRepository, DaysRepository

class ApiClient:
    '''Клиент для работы с сервером.'''
    def __init__(self):
        self._db = Database()
        self._tasks_repo = TasksRepository(self._db)
        self._days_repo = DaysRepository(self._db)
        self._logger = logging.getLogger('ApiClient')

    # Методы для работы с задачами

    def get_all_tasks(self) -> List[Task]:
        '''Получить все задачи.'''
        self._logger.debug('Запрос к серверу на получение всех задач')
        return self._tasks_repo.fetch_all()

    def create_task(self, date: Date, name: str, type_id: str) -> Task:
        '''Создать задачу.'''
        self._logger.debug(f'Запрос к серверу на создание новой задачи с именем {name} типа {type_id} на {date}')
        return self._tasks_repo.create(date, name, type_id)

    def get_task(self, task_id: str) -> Task:
        '''Получить задачу по ID.'''
        self._logger.debug(f'Запрос к серверу на получение задачи {task_id}')
        return self._tasks_repo.get_by_id(task_id)

    def update_task(self, task_id: str, new_name: str) -> Optional[Task]:
        '''Обновить задачу.'''
        self._logger.debug(f'Запрос к серверу на обновление задачи {task_id} с новым названием {new_name}')
        return self._tasks_repo.update(task_id, new_name)

    def get_tasks_for_day(self, date: Date) -> List[Task]:
        '''Получить все задачи за день.'''
        self._logger.debug(f'Запрос к серверу на получение задач на {date}')
        return self._tasks_repo.get_for_day(date)

    def delete_task(self, task_id: str) -> Optional[Task]:
        '''Удалить задачу.'''
        self._logger.debug(f'Запрос к серверу на удаление задачи по ID {task_id}')
        task = self._tasks_repo.delete(task_id)

        days = self.get_all_days()
        for day in days:
            if task.id in day.completed_tasks:
                self.update_task_status(day.date, task.id)

        return task

    # Методы для работы с днями

    def get_all_days(self) -> List[Day]:
        '''Получить все дни.'''
        self._logger.debug('Запрос к серверу на получение всех дней')
        return self._days_repo.fetch_all()

    def get_day(self, date: Date) -> Optional[Day]:
        '''Получить день по дате.'''
        self._logger.debug(f'Запрос к серверу на получение класса дня на {date}')
        return self._days_repo.get_by_date(date)

    def save_day(self, day: Day):
        '''Сохранить день.'''
        self._logger.debug(f'Запрос к серверу на сохранения класса дня на {day.date}')
        return self._days_repo.save(day)

    def delete_day(self, date: Date) -> Optional[Day]:
        '''Удалить день.'''
        self._logger.debug(f'Запрос к серверу на удаление класса дня на {date}')
        return self._days_repo.delete(date)

    def update_task_status(self, date: Date, task_id: str):
        '''Обновить статус задачи.'''
        self._logger.debug(f'Запрос к серверу на обновление статуса задачи {task_id} на {date}')
        return self._days_repo.update_task_status(date, task_id)
