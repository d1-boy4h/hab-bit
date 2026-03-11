from datetime import date as Date

class Task:
    '''Класс задачи (её id, имени и даты).'''
    def __init__(
            self,
            task_id: str,
            name: str,
            date: Date | str,
            type_id: str
        ):
        self._id = task_id
        self._name = name
        self._date = date
        self._type_id = type_id

        if isinstance(date, str):
            self._date = Date.fromisoformat(date)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def date(self):
        return self._date

    @property
    def type_id(self):
        return self._type_id

    def to_dict(self):
        return {
            'task_id': self.id,
            'name': self.name,
            'date': str(self.date),
            'type_id': self.type_id
        }
