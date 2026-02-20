from datetime import datetime, date, timedelta
from ..models import Day

class DaysManager:
    '''Менеджер управления днями, календарём и датами.'''
    def __init__(self, client, task_list):
        self._client = client
        self._task_list = task_list

        self._days_storage = self._client.fetch_days()

        self.selected_date = self.today
        self.month = self.selected_date.month
        self.year = self.selected_date.year

        self.calendar = self.get_calendar(self.month, self.year)

    @property
    def today(self) -> date:
        '''Возвращает сегодняшнюю дату.'''
        return date.today()

    def get_id(self) -> float:
        '''Получение timestamp для уникальных id.'''
        return str(int(datetime.timestamp(datetime.today()) * 10))

    def _is_day_saved(self, day) -> bool:
        '''Проверка, что день сохранён.'''
        for day in self._days_storage:
            if day.date == day.date:
                return True

        return False

    def update_day(self, day, task_id):
        '''Изменяет статус задачи выбранного дня.'''
        if self.selected_date != self.today:
            return

        day.tasks[task_id] = not day.tasks[task_id]

        if self.is_any_task_completed(day):
            if not self._is_day_saved(day):
                self._days_storage.append(day)
        else:
            self.delete_day(day)

        self._client.dump_days(self._days_storage)

    def delete_day(self, day: Day):
        '''Удаляет день.'''
        for index, d in enumerate(self._days_storage):
            if d.date == day.date:
                del self._days_storage[index]

    def _define_tasks_for_day(self, day: Day) -> None:
        '''Перебор задач и выдача их дню.'''
        for task in self._task_list:
            # if task.id in day.tasks:
            #     continue

            if day.date >= task.date:
                day.tasks[task.id] = False

    def get_calendar(self, month: int, year: int) -> list[Day]:
        '''Возвращает массив дней (класс Day) текущего месяца.'''
        first_day = date(year, month, 1)
        weekday = first_day.weekday()

        if weekday:
            first_day -= timedelta(days=weekday)

        # Получаем массив дней месяца
        day_list = [Day(first_day + timedelta(days=d)) for d in range(0, 42)]

        # Подгружаем существующие дни и заменяем ими дни календаря,
        # попутно распределяя задачи
        for day_index, day in enumerate(day_list):
            self._define_tasks_for_day(day)
            for saved_day in self._days_storage:
                if day.date == saved_day.date:
                    day_list[day_index] = saved_day

        # Преобразуем массив месяца в массив недель и возвращаем
        # return [day_list[week*7-7:week*7] for week in range(1, 7)]

        return day_list

    def update_calendar(self):
        self.calendar = self.get_calendar(self.month, self.year)

    def is_day_completed(self, day: Day) -> bool:
        '''Проверка, что все задачи дня выполнены.'''
        return all(day.tasks.values())

    def is_any_task_completed(self, day: Day) -> bool:
        '''Проверка, что хотя-бы одна задача дня выполнена.'''
        return any(day.tasks.values())

    def is_selected_date_is_today(self) -> bool:
        '''Проверка, что выбранный день являяется сегодняшним.'''
        return self.selected_date == self.today

    def change_selected_date(self, string_date: str):
        '''Смена выбранного дня.'''
        date_obj = date.fromisoformat(string_date)

        if self.selected_date != date_obj:
            self.selected_date = date_obj
