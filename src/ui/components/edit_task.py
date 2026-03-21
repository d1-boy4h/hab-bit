from typing import Optional
from ...constants import Navigation, EditTaskActions

class EditTask:
    '''Компонент редактирования задачи.'''
    def __init__(self, console, api_client, store, router):
        self._console = console
        self._api_client = api_client
        self._store = store
        self._router = router

        self._actions =  [
            EditTaskActions.SWITCH,
            EditTaskActions.MOVE,
            EditTaskActions.RENAME,
            EditTaskActions.DELETE,
            EditTaskActions.BACK
        ]

    def _get_action_word(self, action: str) -> Optional[str]:
        '''Возвращает действие в виде слова.'''
        switch_str = 'Выполнить'
        day = self._api_client.get_day(self._store.selected_date)
        if self._store.selected_task_id in day.completed_tasks:
            switch_str = 'Отменить выполнение'

        actions_word_list = {
            EditTaskActions.SWITCH: switch_str,
            EditTaskActions.MOVE: 'Переместить в конец',
            EditTaskActions.RENAME: 'Переименовать',
            EditTaskActions.DELETE: 'Удалить',
            EditTaskActions.BACK: 'Назад'
        }

        if action in actions_word_list:
            return actions_word_list[action]

    def _get_style_for_action(self, action: str) -> str:
        '''Возвращает стилизацию для действия списка редактивования задачи.'''
        style = 'black on white'

        if action == self._store.edit_task_selected_action:
            return style

        return ''

    def render(self):
        '''Отрисовка компонента редактирования задачи.'''
        if self._router.current_route != Navigation.EDIT_TASK:
            return

        current_task = self._api_client.get_task(self._store.selected_task_id)
        self._console.print(
            f'Редактирование задачи \'{current_task.name}\'',
            style='bold blue'
        )

        for action in self._actions:
            self._console.print(
                self._get_action_word(action),
                style=self._get_style_for_action(action)
            )
