from datetime import date as Date

class Day:
    '''Класс дня с датой и списком выполненных задач.'''
    def __init__(self, date, task_list=None):
        if isinstance(date, Date):
            self._date = date
        elif isinstance(date, str):
            self._date = Date.fromisoformat(date)
        self._task_list = task_list if task_list else {}

    @property
    def date(self):
        return self._date

    @property
    def task_list(self):
        return self._task_list

    def to_dict(self):
        return {
            'date': str(self.date),
            'task_list': self.task_list
        }
