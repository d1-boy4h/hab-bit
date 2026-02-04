from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Horizontal, Vertical

from .widgets import CalendarWidget, TasksWidget
from ..constants import PROGRAM_NAME, PROGRAM_VERSION

class Interface(App):
    '''Интерфейс (TUI).'''
    CSS_PATH = '../styles/main.tcss'

    def __init__(self, task_manager, days_manager):
        self._task_manager = task_manager
        self._days_manager = days_manager

        super().__init__()
        self.title = f'{PROGRAM_NAME} [v{PROGRAM_VERSION}]'

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Horizontal():
            with Vertical():
                tasks_widget = TasksWidget(
                    self._task_manager,
                    self._days_manager,
                )

                calendar_widget = CalendarWidget(
                    self._days_manager,
                    tasks_widget
                )

                yield calendar_widget
            with Vertical():
                yield tasks_widget

        yield Footer()
