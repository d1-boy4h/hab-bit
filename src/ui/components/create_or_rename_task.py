from ...constants import Navigation, TaskType

class CreateOrRenameTask:
    '''Компонент создания задачи.'''
    def __init__(self, console, api_client, store, router):
        self._console = console
        self._api_client = api_client
        self._store = store
        self._router = router

        self._valid_nav_list = [
            Navigation.CREATE_TASK,
            Navigation.CREATE_SINGLE_TASK,
            Navigation.RENAME_TASK
        ]

    def render(self):
        '''Отрисовка компонента создания задачи.'''
        if self._router.current_route not in self._valid_nav_list:
            return

        if self._router.current_route == Navigation.CREATE_TASK:
            task_name = self._console.input('Введите название привычки: ')
            date = self._store.selected_date
            self._api_client.create_task(date, task_name, TaskType.EVERYDAY)

        elif self._router.current_route == Navigation.CREATE_SINGLE_TASK:
            task_name = self._console.input('Введите название задачи: ')
            date = self._store.selected_date
            self._api_client.create_task(date, task_name, TaskType.SINGLE)

        elif self._router.current_route == Navigation.RENAME_TASK:
            task_name = self._console.input('Введите новое название задачи: ')
            self._api_client.update_task(
                self._store.selected_task_id,
                task_name
            )

        self._router.navigate(Navigation.TASK_LIST)
