from datetime import datetime, date, timedelta
from ..models import Day, Task

class DaysManager:
    '''Менеджер управления днями, календарём и датами.'''
    def __init__(self, client, task_list):
        self._client = client
        self._task_list = task_list

        self._days_storage = self._client.fetch_days()

        self.selected_date = self.today
        self.selected_month = self.today.month
        self.selected_year = self.today.year

        self.calendar = self.get_calendar(
            self.selected_month,
            self.selected_year
        )

    @property
    def today(self) -> date:
        '''Возвращает сегодняшнюю дату.'''
        return date.today()

    def get_id(self) -> float:
        '''Получение timestamp для уникальных id.'''
        return str(int(datetime.timestamp(datetime.today()) * 10))

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

    def get_calendar(self, month: int, year: int) -> list[date]:
        '''Возвращает массив дней в виде дат текущего месяца.'''
        first_day = date(year, month, 1)
        weekday = first_day.weekday()

        if weekday:
            first_day -= timedelta(days=weekday)

        # Получаем массив дней месяца
        return [first_day + timedelta(days=d) for d in range(0, 42)]

    def get_tasks_for_day(self, date: date) -> list[Task]:
        '''Возвращает задачи определённого дня.'''
        return [task for task in self._task_list if task.date <= date]

    def is_day_completed(self, date: date) -> bool:
        '''Проверка, что все задачи дня выполнены.'''
        tasks = self.get_tasks_for_day(date)
        if not len(tasks):
            return True

        day = self.get_day(date)
        if day:
            return len(tasks) == len(day.completed_tasks)

    def change_selected_date(self, str_date: str):
        '''Смена выбранного дня.'''
        new_date = date.fromisoformat(str_date)

        if self.selected_date != new_date:
            self.selected_date = new_date
