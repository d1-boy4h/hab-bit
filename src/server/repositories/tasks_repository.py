from typing import List, Optional
from datetime import date as Date
import uuid

from ...models import Task
from .. import Database

class TasksRepository:
    '''Репозиторий задач.'''
    def __init__(self, db: Database):
        self._db = db
        self._table_name = 'tasks'

    def _to_model(self, data: dict) -> Task:
        '''Преобразует словарь из JSON в задачу.'''
        return Task(**data)

    def _from_model(self, task: Task) -> dict:
        '''Преобразовазует задачу в словарь для JSON.'''
        return task.to_dict()

    def fetch_all(self) -> List[Task]:
        '''Возвращает все задачи.'''
        data = self._db.read_table(self._table_name)
        return [self._to_model(item) for item in data]

    def create(self, date: Date, name: str) -> Task:
        '''Создаёт новую задачу.'''
        tasks = self.fetch_all()

        new_task = Task(str(uuid.uuid4()), name, date=str(date))
        tasks.append(new_task)

        data = [self._from_model(task) for task in tasks]
        self._db.write_table(self._table_name, data)

        return new_task

    def get_by_id(self, task_id: str) -> Optional[Task]:
        '''Ищет задачу по ID.'''
        tasks = self.fetch_all()
        for task in tasks:
            if task.id == task_id:
                return task

    def update(self, task_id: str, new_name: str) -> Optional[Task]:
        '''Обновляет задачу.'''
        tasks = self.fetch_all()

        for task in tasks:
            if task.id == task_id:
                task.name = new_name

                data = [self._from_model(t) for t in tasks]
                self._db.write_table(self._table_name, data)

                return task

    def delete(self, task_id: str) -> Optional[Task]:
        '''Удаляет задачу.'''
        tasks = self.fetch_all()

        for i, task in enumerate(tasks):
            if task.id == task_id:
                deleted = tasks.pop(i)

                data = [self._from_model(t) for t in tasks]
                self._db.write_table(self._table_name, data)

                return deleted

    def get_for_day(self, date: Date) -> List[Task]:
        '''Вощвращает список задач за определённый день.'''
        tasks = self.fetch_all()
        return [task for task in tasks if task.date <= date]
