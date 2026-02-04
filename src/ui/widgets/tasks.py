from textual.widget import Widget
from textual.widgets import Static, Checkbox, Input
from textual.containers import Vertical

class TasksWidget(Widget):
    '''Виджет списка задач.'''
    def __init__(self, task_manager, days_manager):
        self._task_manager = task_manager
        self._days_manager = days_manager

        super().__init__()

    @property
    def _selected_day(self):
        '''Возвращает объект дня из кликнутого дня на календаре.'''
        for week in self._days_manager.calendar:
            for day in week:
                if day.date == self._days_manager.selected_date:
                    return day

    def compose(self):
        yield Static('', id='tasks-title', classes='title')
        yield Vertical(id='tasks-container')
        yield Input(id='tasks-input')

    def on_mount(self):
        self.build()

    def build(self):
        '''Рендер виджета.'''
        title = self.query_one('#tasks-title')
        title.update(f'Список задач на {self._selected_day.date.day} число:')

        container = self.query_one('#tasks-container')
        container.remove_children()

        tasks = self._get_tasks_for_day(self._selected_day)

        if not len(tasks):
            container.mount(Static('Задач на это число не запланировано.'))

        is_today = self._days_manager.is_selected_date_is_today()
        for task in tasks:
            container.mount(Checkbox(
                task.name,
                value=self._selected_day.task_list[task.id],
                id=f'task-{task.id}-{self._days_manager.get_id()}',
                classes='task_checkbox',
                disabled=not is_today
            ))

        tasks_input = self.query_one('#tasks-input')
        tasks_input.disabled = not is_today

    def _get_tasks_for_day(self, day):
        '''Возвращает задачи определённого дня.'''
        return [self._task_manager.get_task(task_id)
            for task_id in day.task_list.keys()
        ]

    def on_checkbox_changed(self, event: Checkbox.Changed):
        task_id = event.checkbox.id.split('-')[1]
        self._days_manager.update_day(self._selected_day, task_id)

    def on_input_submitted(self, event: Input.Submitted):
        if event.input.id != 'tasks-input':
            return

        self._task_manager.create_task(event.value)
        event.control.clear()
        self.build()
