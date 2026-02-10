from datetime import date as Date

class Task:
    '''Класс задачи (её id, имени и даты).'''
    def __init__(self, id, name='', date=None):
        self._id = str(id)
        self._name = name
        self._date = Date.fromisoformat(date) if date else Date.today()

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

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': str(self.date)
        }
