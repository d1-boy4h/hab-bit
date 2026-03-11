from datetime import date as Date
from ...constants import Navigation, TaskListActions

class TaskList:
    '''Компонента списка задач.'''
    def __init__(self, console, api_client, store, router):
        self._console = console
        self._api_client = api_client
        self._store = store
        self._router = router

        self._title_style = 'bold blue'

    def _get_style_for_action(self, action: str) -> str:
        '''Возвращает стилизацию для элемента списка задач.'''
        style = 'black on white'

        if self._router.current_route == Navigation.CALENDAR and \
            self._store.selected_date < Date.today():
            return 'grey46'

        if action == self._store.tasklist_selected_action:
            return style

        return ''

    def render(self):
        '''Отрисовка компонента списка задач.'''
        self._console.print(
            f'Список задач на {self._store.selected_date.day} число',
            style=self._title_style
        )

        # Действие назад
        if self._store.selected_date >= Date.today() and \
            self._router.current_route != Navigation.CALENDAR:
            self._console.print(
                '- Назад -',
                style=self._get_style_for_action(TaskListActions.BACK)
            )

        # Отрисовка задач
        tasks = self._api_client.get_tasks_for_day(self._store.selected_date)

        if tasks:
            for index, task in enumerate(tasks):
                selected_task_style = self._get_style_for_action(task.id)
                self._console.print(
                    f'{index + 1}. {task.name}',
                    style=selected_task_style
                )
        elif self._router.current_route == Navigation.CALENDAR:
            self._console.print('На этот день задач не найдено.')

        # Добавление новой задачи
        if self._store.selected_date >= Date.today() and \
            self._router.current_route != Navigation.CALENDAR:
            self._console.print(
                '- Создать новую -',
                style=self._get_style_for_action(TaskListActions.CREATE)
            )
