from rich.console import Console
from rich.theme import Theme
import readchar

from .components import Header, Calendar, TaskList, TaskCreation, EditTask

class Interface():
    '''Интерфейс (TUI).'''
    def __init__(self, api_client, store, router, keyboard_handler):
        self._api_client = api_client
        self._store = store
        self._router = router
        self._keyboard_handler = keyboard_handler

        # Отмена тем, чтобы правильно работали стили
        custom_theme = Theme(inherit=False)
        self._console = Console(theme=custom_theme)

        # Инициализация компонентов
        self._header = Header(self._console)
        self._calendar = Calendar(
            self._console,
            self._api_client,
            self._store,
            self._router
        )
        self._tasklist = TaskList(
            self._console,
            self._api_client,
            self._store,
            self._router
        )
        self._task_creation = TaskCreation(
            self._console,
            self._api_client,
            self._router
        )
        self._edit_task = EditTask(
            self._console,
            self._api_client,
            self._store,
            self._router
        )

        # Условие работы главного цикла программы
        self._running = True

    def _render(self):
        '''Главная функция отрисовки интерфейса.'''
        while self._running:
            self._header.render()

            self._console.print('[grey46]Для выхода нажмите \'q\'[/]')
            self._calendar.render()

            self._console.print()
            self._tasklist.render()

            self._console.print()
            self._edit_task.render()

            key = readchar.readkey()
            self._keyboard_handler.handle(key)

            self._console.print()
            self._task_creation.render()

            self._console.clear()

    def run(self):
        '''Запуск интерфейса программы.'''
        try:
            with self._console.screen():
                self._render()
        except KeyboardInterrupt:
            self._exit()

    def _exit(self):
        '''Выход из программы.'''
        self._running = False
        self._console.print('[white on blue bold]До свидания![/]')
