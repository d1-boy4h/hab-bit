from datetime import date as Date
from typing import Optional

class Store:
    '''Хранилище состояний приложения.'''
    def __init__(self):
        self.selected_date: Date = Date.today()
        self.tasklist_selected_action: Optional[str] = None
        # self.selected_task_id: Optional[str] = None
