from datetime import date as Date
from ...constants import Navigation, TaskListActions
from ...models import Day

class TaskList:
    '''Компонента списка задач.'''
    def __init__(self, console, api_client, store, router):
        self._console = console
        self._api_client = api_client
        self._store = store
        self._router = router

    def _get_style_for_action(
            self,
            action: str,
            day: Day = None
        ) -> str:
        '''Возвращает стилизацию для элемента списка задач.'''
        color_style = ''
        strike_style = ''

        if day:
            task_id = action
            if task_id in day.completed_tasks:
                if self._store.selected_date < Date.today():
                    color_style = 'green'
                else:
                    color_style = 'green'
                    strike_style = 'strike'
            else:
                if self._store.selected_date < Date.today():
                    color_style = 'grey46'

        if action == self._store.tasklist_selected_action:
            color_style = 'black on white'

        return f'{strike_style} {color_style}'

    def render(self):
        '''Отрисовка компонента списка задач.'''
        if self._router.current_route == Navigation.EDIT_TASK:
            return

        self._console.print(
            f'Список задач на {self._store.selected_date.day} число',
            style='bold blue'
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
        day = self._api_client.get_day(self._store.selected_date)

        if tasks:
            for index, task in enumerate(tasks):
                selected_task_style = self._get_style_for_action(task.id, day)
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
