from typing import List, Optional
from datetime import date as Date

from ..models import Task, Day
from ..server import Database, TasksRepository, DaysRepository

class ApiClient:
    '''Клиент для работы с сервером.'''
    def __init__(self):
        self._db = Database()
        self._tasks_repo = TasksRepository(self._db)
        self._days_repo = DaysRepository(self._db)

    # Методы для работы с задачами

    def get_all_tasks(self) -> List[Task]:
        '''Получить все задачи.'''
        return self._tasks_repo.fetch_all()

    def create_task(self, date: Date, name: str) -> Task:
        '''Создать задачу.'''
        return self._tasks_repo.create(date, name)

    def get_task(self, task_id: str) -> Task:
        '''Получить задачу по ID.'''
        return self._tasks_repo.get_by_id(task_id)

    def update_task(self, task_id: str, new_name: str) -> Optional[Task]:
        '''Обновить задачу.'''
        return self._tasks_repo.update(task_id, new_name)

    def get_tasks_for_day(self, date: Date) -> List[Task]:
        '''Получить все задачи за день.'''
        return self._tasks_repo.get_for_day(date)

    # Методы для работы с днями

    def get_all_days(self) -> List[Day]:
        '''Получить все дни.'''
        return self._days_repo.fetch_all()

    def get_day(self, date: Date) -> Optional[Day]:
        '''Получить день по дате.'''
        return self._days_repo.get_by_date(date)

    def save_day(self, day: Day):
        '''Сохранить день.'''
        return self._days_repo.save(day)

    def delete_day(self, date: Date) -> Optional[Day]:
        '''Удалить день.'''
        return self._days_repo.delete(date)

    def update_task_status(self, date: Date, task_id: str):
        '''Обновить статус задачи.'''
        return self._days_repo.update_task_status(date, task_id)
