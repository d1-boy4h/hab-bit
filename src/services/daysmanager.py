from datetime import date
from ..models import Day, Task

class DaysManager:
    '''Менеджер управления днями, календарём и датами.'''
    def __init__(self, client):
        self._client = client
        self._days_storage = self._client.fetch_days()

    def get_new_day(self, date: date) -> Day:
        return Day(date)

    def get_day(self, date: date) -> Day | None:
        '''Получение дня по дате из БД.'''
        for saved_day in self._days_storage:
            if date == saved_day.date:
                return saved_day

    def update_task_status_for_day(self, task_id: str):
        '''Изменяет статус задачи выбранного дня и сохраняет в БД.'''
        if self.selected_date != self.today:
            return

        day = self.get_day(self.selected_date)

        if day:
            if task_id in day.completed_tasks:
                day.completed_tasks.remove(task_id)
            else:
                day.completed_tasks.append(task_id)

            if not day.completed_tasks:
                self._days_storage.remove(day)
                
        else:
            new_day = Day(self.selected_date)
            self._days_storage.append(new_day)
            new_day.completed_tasks.append(task_id)

        self._client.dump_days(self._days_storage)
