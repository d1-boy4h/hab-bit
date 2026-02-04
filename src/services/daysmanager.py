from datetime import datetime, date, timedelta
from ..models import Day

class DaysManager:
    '''Менеджер управления днями, календарём и датами.'''
    def __init__(self, storage, tasks):
        self._storage = storage
        self._task_list = tasks

        self._days = storage.fetch_days()

        self.selected_date = self.today
        self.month = self.selected_date.month
        self.year = self.selected_date.year

    @property
    def today(self) -> date:
        '''Возвращает сегодняшнюю дату.'''
        return date.today()

    @property
    def calendar(self):
        '''Обёртка метода get_calendar для удобства.'''
        return self.get_calendar(self.month, self.year)

    def get_id(self) -> float:
        '''Получение timestamp для уникальных id.'''
        return str(int(datetime.timestamp(datetime.today()) * 10))

    def _is_day_exist(self, day) -> bool:
        '''Проверка, что день сохранён.'''
        for saved_day in self._days:
            if day.date == saved_day.date:
                return True

        return False

    def update_day(self, day, task_id):
        '''Изменяет статус задачи выбранного дня.'''
        if self.selected_date != self.today:
            return

        day.task_list[task_id] = not day.task_list[task_id]

        if self.is_any_task_completed(day):
            if not self._is_day_exist(day):
                self._days.append(day)
            self._storage.dump_days(self._days)
        else:
            self.delete_day(day)
            self._storage.dump_days(self._days)

    def delete_day(self, day):
        '''Удаляет день.'''
        for index, d in enumerate(self._days):
            if d.date == day.date:
                del self._days[index]

    def _define_tasks_for_day(self, day: Day) -> None:
        '''Перебирает задачи и распределяет их выбранному дню по датам.'''
        for task in self._task_list:
            if task.id in day.task_list:
                continue

            if day.date >= task.date:
                day.task_list[task.id] = False

    def get_calendar(self, month: int, year: int) -> list[list[Day]]:
        '''Возвращает календарный массив с массивами недель, каждый из которых содержит по 7 дней (класс Day)'''
        first_day = date(year, month, 1)
        weekday = first_day.weekday()

        if weekday:
            first_day -= timedelta(days=weekday)

        # Составление массива дней месяца
        day_list = [Day(first_day + timedelta(days=d)) for d in range(0, 42)]

        # Подгружаем существующие дни и заменяем ими дни календаря,
        # попутно распределяя задачи
        for day_index, day in enumerate(day_list):
            for saved_day in self._days:
                if day.date == saved_day.date:
                    day_list[day_index] = saved_day

            self._define_tasks_for_day(day)

        # Преобразуем массив месяца в массив недель и возвращаем
        return [day_list[week*7-7:week*7] for week in range(1, 7)]

    def is_day_completed(self, day: Day) -> bool:
        '''Проверка, что все задачи дня выполнены.'''
        return all(day.task_list.values())

    def is_any_task_completed(self, day: Day) -> bool:
        '''Проверка, что хотя-бы одна задача дня выполнена.'''
        return any(day.task_list.values())

    def is_selected_date_is_today(self) -> bool:
        '''Проверка, что выбранный день являяется сегодняшним.'''
        return self.selected_date == self.today

    def change_selected_date(self, string_date: str):
        '''Смена выбранного дня.'''
        date_obj = date.fromisoformat(string_date)

        if self.selected_date != date_obj:
            self.selected_date = date_obj
