from typing import List, Optional
from datetime import date as Date

from ...models import Day
from .. import Database

class DaysRepository:
    '''Репозиторий дней.'''
    def __init__(self, db: Database):
        self._db = db
        self._table_name = 'days'

    def _to_model(self, data: dict) -> Day:
        '''Преобразует словарь из JSON в день.'''
        return Day(**data)

    def _from_model(self, day: Day) -> dict:
        '''Преобразовазует день в словарь для JSON.'''
        return day.to_dict()

    def fetch_all(self) -> List[Day]:
        '''Возвращает все дни.'''
        data = self._db.read_table(self._table_name)
        return [self._to_model(item) for item in data]

    def get_by_date(self, date: Date) -> Day:
        '''Возвращает день по дате'''
        days = self.fetch_all()

        for day in days:
            if day.date == date:
                return day
        
        return Day(date)

    def save(self, day: Day):
        '''Сохраняет или обновляет день.'''
        days = self.fetch_all()

        for i, existing_day in enumerate(days):
            if existing_day.date == day.date:
                days[i] = day
                break

        else:
            days.append(day)

        data = [self._from_model(d) for d in days]
        self._db.write_table(self._table_name, data)

    def delete_by_date(self, date: Date) -> Optional[Day]:
        '''Удаляет день по дате.'''
        days = self.fetch_all()

        for i, day in enumerate(days):
            if day.date == date:
                deleted = days.pop(i)

                data = [self._from_model(d) for d in days]
                self._db.write_table(self._table_name, data)

                return deleted

    def update_task_status(self, date: Date, task_id: str):
        '''Обновляет статус задачи в конкретный день.'''
        day = self.get_by_date(date)

        if not day:
            day = Day(date)

        if task_id not in day.completed_tasks:
            day.completed_tasks.append(task_id)
        elif task_id in day.completed_tasks:
            day.completed_tasks.remove(task_id)

        if not day.completed_tasks:
            self.delete_by_date(date)
        else:
            self.save(day)
