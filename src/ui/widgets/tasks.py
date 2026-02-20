from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static, Checkbox, Input
from textual.containers import Vertical

class TasksWidget(Widget):
    '''Виджет списка задач.'''
    def __init__(self, task_manager, days_manager):
        self._task_manager = task_manager
        self._days_manager = days_manager

        super().__init__()

    # @property
    # def _selected_day(self):
    #     '''Возвращает дату кликнутого дня на календаре.'''
    #     for day_date in self._days_manager.calendar:
    #         if day_date == self._days_manager.selected_date:
    #             return day_date

    def compose(self) -> ComposeResult:
        yield Static('', id='tasks-title', classes='title')
        yield Vertical(id='tasks-container')
        yield Input(id='tasks-input')

    def on_mount(self):
        self.build()

    def build(self):
        '''Рендер виджета.'''
        title = self.query_one('#tasks-title')
        title.update(f'Список задач на {self._days_manager.selected_date.day} число:')

        container = self.query_one('#tasks-container')
        container.remove_children()

        selected_date = self._days_manager.selected_date
        selected_day = self._days_manager.get_day(
            selected_date
        ) or self._days_manager.get_new_day(selected_date)

        tasks = self._days_manager.get_tasks_for_day(
            self._days_manager.selected_date
        )

        if not tasks:
            container.mount(Static('Задач на это число не запланировано.'))

        is_today = self._days_manager.selected_date == self._days_manager.today

        for task in tasks:
            container.mount(Checkbox(
                task.name,
                value=task.id in selected_day.completed_tasks,
                id=f'task-{task.id}-{self._days_manager.get_id()}',
                classes='task_checkbox',
                disabled=not is_today
            ))

        tasks_input = self.query_one('#tasks-input')
        tasks_input.disabled = not is_today

    def on_checkbox_changed(self, event: Checkbox.Changed):
        task_id_decompose = event.checkbox.id.split('-')
        task_id = '-'.join(task_id_decompose[1:-1])

        self._days_manager.update_task_status_for_day(task_id)

    def on_input_submitted(self, event: Input.Submitted):
        if not event.input.id.startswith('tasks-input'):
            return

        self._task_manager.create_task(event.value)
        event.control.clear()
        self.build()
