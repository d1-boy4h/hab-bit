from datetime import date as Date
from ...constants import Navigation, TaskListActions

class TaskList:
    '''Компонента списка задач.'''
    def __init__(self, console, storage):
        self._console = console
        self._storage = storage

        self._title_style = 'bold blue'

    def _get_style_for_action(self, action: str) -> str:
        '''Возвращает стилизацию для элемента списка задач.'''
        style = 'black on white'
        if self._storage.navigation == Navigation.CALENDAR and \
            self._storage.selected_date < Date.today():
            return 'grey46'

        if action == self._storage.tasklist_selected_action:
            return style

        return ''

    def render(self):
        '''Отрисовка компонента списка задач.'''
        self._console.print(
            f'Список задач на {self._storage.selected_date.day} число',
            style=self._title_style
        )

        selected_date = self._storage.selected_date
        # loaded_day = self._days_manager.get_day(
        #     selected_date
        # ) or self._days_manager.get_new_day(selected_date)
        # selected_task = self._storage.selected_task
        # is_navigated = self._storage.navigation == Navigation.task_list

        # Действие назад
        if self._storage.selected_date >= Date.today() and \
            self._storage.navigation != Navigation.CALENDAR:
            self._console.print(
                '- Назад -',
                style=self._get_style_for_action(TaskListActions.BACK)
            )

        # Отрисовка задач
        if self._storage.tasks:
            for index, task in enumerate(self._storage.tasks):
                selected_task_style = self._get_style_for_action(task.id)
                self._console.print(
                    f'{index + 1}. {task.name}',
                    style=selected_task_style
                )
        elif self._storage.navigation == Navigation.CALENDAR:
            self._console.print('На этот день задач не найдено.')

        # Добавление новой задачи
        if self._storage.selected_date >= Date.today() and \
            self._storage.navigation != Navigation.CALENDAR:
            self._console.print(
                '- Создать новую -',
                style=self._get_style_for_action(TaskListActions.CREATE)
            )
