from ..ui import Interface
from ..api import Client
from ..services import TaskManager, DaysManager

class App:
    '''Ядро программы.'''
    def __init__(self):
        self._client = Client()

    def run(self):
        task_manager = TaskManager(self._client)
        days_manager = DaysManager(self._client, task_manager.tasks)

        interface = Interface(task_manager, days_manager)
        interface.run()
