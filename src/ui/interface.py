from rich.console import Console
from rich.theme import Theme

from .components import Header, Calendar, TaskList

class Interface():
    '''Интерфейс (TUI).'''
    def __init__(self, storage):
        self._storage = storage

        # Отмена тем, чтобы правильно работали стили
        custom_theme = Theme(inherit=False)
        self._console = Console(theme=custom_theme)

        # Инициализация компонентов
        self._header = Header(self._console)
        self._calendar = Calendar(self._console, self._storage)
        self._tasklist = TaskList(self._console, self._storage)

        # Условие работы главного цикла программы
        self._running = True

    def _render(self):
        '''Главная функция отрисовки интерфейса.'''
        while self._running:
            self._header.render()

            self._console.print()
            self._calendar.render()

            self._console.print()
            self._tasklist.render()

            self._storage.key_handler()
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
