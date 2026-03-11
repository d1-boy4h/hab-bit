import readchar
from datetime import date as Date, timedelta
from rich.console import Console

from ..constants import Navigation, TaskListActions

class Storage:
    '''Хранилище состояний интерфейса.'''
    def __init__(self, tasks_manager, days_manager):
        self.days_manager = days_manager
        self.tasks_manager = tasks_manager

        self.selected_date = Date.today()

        self.navigation = Navigation.CALENDAR

        self._tasklist_actions = self._get_clear_taslist_actions()
        self._tasklist_selected_action_index = 0
    
    def _get_clear_taslist_actions(self) -> list[str]:
        '''Возвращает чистый список действий для списка задач.'''
        return [
            TaskListActions.BACK,
            TaskListActions.CREATE
        ]

    def _get_tasklist_actions(self) -> list[str]:
        '''Возвращает заполненный задачами список действий для списка задач.'''
        tasklist_actions = self._get_clear_taslist_actions()
        for index, task in enumerate(self.tasks):
            tasklist_actions.insert(index + 1, task.id)
        
        return tasklist_actions

    @property
    def tasklist_selected_action(self):
        '''Возвращает выбранное действие в списке задач.'''
        return self._tasklist_actions[self._tasklist_selected_action_index]

    @property
    def tasks(self):
        '''Возвращает задачи за день выделенной даты.'''
        return self.tasks_manager.get_tasks_for_day(
            self.selected_date
        )

    # TODO: ТехДолг, оптимизировать работу клиента и сервера
    def is_day_completed(self, date: Date) -> bool:
        '''Проверка, что все задачи дня выполнены.'''
        tasks = self.tasks_manager.get_tasks_for_day(date)
        if not tasks:
            return True

        day = self.days_manager.get_day(date)
        if day:
            return len(tasks) == len(day.completed_tasks)

    def key_handler(self):
        '''Перехват клавиш и вызов функций для них.'''
        key = readchar.readkey()

        if key == 'q':
            # Вызов self._exit() через ошибку
            raise KeyboardInterrupt

        elif self.navigation == Navigation.CALENDAR:
            if key == readchar.key.RIGHT:
                self.selected_date += timedelta(days=1)
            elif key == readchar.key.LEFT:
                self.selected_date -= timedelta(days=1)
            elif key == readchar.key.DOWN:
                self.selected_date += timedelta(days=7)
            elif key == readchar.key.UP:
                self.selected_date -= timedelta(days=7)
            elif key == readchar.key.ENTER:
                if self.selected_date >= Date.today():
                    self.navigation = Navigation.TASK_LIST
                    self._tasklist_actions = self._get_tasklist_actions()

        elif self.navigation == Navigation.TASK_LIST:
            if key == readchar.key.DOWN:
                self._tasklist_selected_action_index += 1
                if self._tasklist_selected_action_index == len(
                    self._tasklist_actions
                ):
                    self._tasklist_selected_action_index = 0

            elif key == readchar.key.UP:
                self._tasklist_selected_action_index -= 1
                if self._tasklist_selected_action_index == -1:
                    self._tasklist_selected_action_index = len(
                        self._tasklist_actions
                    ) - 1

            elif key == readchar.key.ENTER:
                if self.tasklist_selected_action == TaskListActions.BACK:
                    self.navigation = Navigation.CALENDAR
                    self._tasklist_actions = self._get_clear_taslist_actions()

                elif self.tasklist_selected_action == TaskListActions.CREATE:
                    console = Console()
                    console.print()

                    task_name = console.input('Введите название задачи: ')
                    self.tasks_manager.create_task(task_name)

                    self._tasklist_actions = self._get_tasklist_actions()
