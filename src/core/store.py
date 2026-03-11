from datetime import date as Date
from typing import Optional

class Store:
    '''Хранилище состояний приложения.'''
    selected_date: Date
    tasklist_selected_action: Optional[str]
    selected_task_id: Optional[str]
    edit_task_selected_action: Optional[str]

    def __init__(self):
        self.selected_date = Date.today()
        self.tasklist_selected_action = None
        self.selected_task_id = None
        self.edit_task_selected_action = None
