from datetime import date as Date

class Day:
    '''Класс дня с датой и списком выполненных задач.'''
    def __init__(self, date, tasks=None):
        if isinstance(date, str):
            self._date = Date.fromisoformat(date)
        else:
            self._date = date

        self._tasks = tasks if tasks else {}

    @property
    def date(self):
        return self._date

    @property
    def tasks(self):
        return self._tasks

    def to_dict(self):
        return {
            'date': str(self.date),
            'tasks': self.tasks
        }
