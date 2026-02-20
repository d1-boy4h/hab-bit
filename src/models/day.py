from datetime import date as Date

class Day:
    '''Класс дня с датой и списком выполненных задач.'''
    def __init__(self, date, completed_tasks=None):
        if isinstance(date, str):
            self._date = Date.fromisoformat(date)
        else:
            self._date = date

        self._completed_tasks = completed_tasks if completed_tasks else []

    @property
    def date(self):
        return self._date

    @property
    def completed_tasks(self):
        return self._completed_tasks

    def to_dict(self):
        return {
            'date': str(self.date),
            'completed_tasks': self.completed_tasks
        }
