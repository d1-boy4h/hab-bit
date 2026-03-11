from ...constants import Navigation

class TaskCreation:
    '''Компонент создания задачи.'''
    def __init__(self, console, api_client, router):
        self._console = console
        self._api_client = api_client
        self._router = router

    def render(self):
        '''Отрисовка компонента создания задачи.'''
        if self._router.current_route != Navigation.CREATE_TASK:
            return
        
        task_name = self._console.input('Введите название задачи: ')
        self._api_client.create_task(task_name)
        self._router.navigate(Navigation.TASK_LIST)
