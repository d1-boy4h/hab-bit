from typing import Any
import readchar
from datetime import date as Date, timedelta

from ..constants import Navigation, TaskListActions, EditTaskActions

class KeyboardHandler:
    '''Обработчик клавиатурного ввода.'''
    def __init__(self, api_client: Any, store: Any, router: Any):
        self.api_client = api_client
        self.store = store
        self.router = router

    def handle(self, key: str):
        '''Обработка нажатия клавиши.'''
        if key in ['q', 'й']:
            # Вызов self._exit() через ошибку
            raise KeyboardInterrupt

        if self.router.current_route == Navigation.CALENDAR:
            self._handle_calendar(key)
        elif self.router.current_route == Navigation.TASK_LIST:
            self._handle_task_list(key)
        elif self.router.current_route == Navigation.EDIT_TASK:
            self._handle_edit_task(key)

    def _handle_calendar(self, key: str):
        '''Обработка клавиш в режиме календаря.'''
        if key == readchar.key.RIGHT:
            self.store.selected_date += timedelta(days=1)
        elif key == readchar.key.LEFT:
            self.store.selected_date -= timedelta(days=1)
        elif key == readchar.key.DOWN:
            self.store.selected_date += timedelta(days=7)
        elif key == readchar.key.UP:
            self.store.selected_date -= timedelta(days=7)
        elif key == readchar.key.ENTER:
            if self.store.selected_date >= Date.today():
                self.router.navigate(Navigation.TASK_LIST)
                self.store.tasklist_selected_action = TaskListActions.BACK

    def _get_tasklist_actions(self) -> list[str]:
        '''Возвращает список доступных действий в списке задач.'''
        actions = [TaskListActions.BACK]

        tasks = self.api_client.get_tasks_for_day(self.store.selected_date)
        for task in tasks:
            actions.append(task.id)

        if self.store.selected_date >= Date.today():
            actions.append(TaskListActions.CREATE)

        return actions

    def _handle_task_list(self, key: str):
        '''Обработка клавиш в режиме списка задач.'''
        actions = self._get_tasklist_actions()
        current_index = actions.index(self.store.tasklist_selected_action)

        if key == readchar.key.DOWN:
            new_index = (current_index + 1) % len(actions)
            self.store.tasklist_selected_action = actions[new_index]

        elif key == readchar.key.UP:
            new_index = (current_index - 1) % len(actions)
            self.store.tasklist_selected_action = actions[new_index]

        if key == readchar.key.ENTER:
            selected = self.store.tasklist_selected_action

            if selected == TaskListActions.BACK:
                self.router.navigate(Navigation.CALENDAR)

            elif selected == TaskListActions.CREATE:
                self.router.navigate(Navigation.CREATE_TASK)

            else:
                self.store.selected_task_id = selected
                self.router.navigate(Navigation.EDIT_TASK)
                self.store.edit_task_selected_action = EditTaskActions.SWITCH

    def _handle_edit_task(self, key: str):
        '''Обработка клавиш в режиме редактирования задачи.'''
        actions = [
            EditTaskActions.SWITCH,
            EditTaskActions.RENAME,
            EditTaskActions.DELETE,
            EditTaskActions.BACK
        ]
        current_index = actions.index(self.store.edit_task_selected_action)

        if key == readchar.key.DOWN:
            new_index = (current_index + 1) % len(actions)
            self.store.edit_task_selected_action = actions[new_index]

        elif key == readchar.key.UP:
            new_index = (current_index - 1) % len(actions)
            self.store.edit_task_selected_action = actions[new_index]

        if key == readchar.key.ENTER:
            selected = self.store.edit_task_selected_action

            if selected == EditTaskActions.BACK:
                self.router.navigate(Navigation.TASK_LIST)

            elif selected == EditTaskActions.SWITCH:
                self.api_client.update_task_status(
                    self.store.selected_date,
                    self.store.selected_task_id
                )
                self.router.navigate(Navigation.TASK_LIST)

            elif selected == EditTaskActions.RENAME:
                self.router.navigate(Navigation.RENAME_TASK)

            elif selected == EditTaskActions.DELETE:
                self.api_client.delete_task(self.store.selected_task_id)
                self.store.tasklist_selected_action = TaskListActions.BACK
                self.router.navigate(Navigation.TASK_LIST)