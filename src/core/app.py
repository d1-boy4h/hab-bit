from ..ui import Interface
from ..stores import Storage
from ..services import TaskManager, DaysManager

class App:
    '''Ядро программы.'''
    def __init__(self):
        self._storage = Storage()

    def run(self):
        task_manager = TaskManager(self._storage)
        days_manager = DaysManager(self._storage, task_manager.tasks)

        interface = Interface(task_manager, days_manager)
        interface.run()
