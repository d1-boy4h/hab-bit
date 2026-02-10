from ..models import Task
import uuid

class TaskManager:
    '''Менеджер управления задачами (CRUD).'''
    def __init__(self, storage):
        self._storage = storage
        self._tasks = storage.fetch_tasks()

    def create_task(self, name):
        '''Создание задачи.'''
        new_task = Task(uuid.uuid4(), name)
        self._tasks.append(new_task)
        self._storage.dump_tasks(self._tasks)

        return new_task

    def get_task(self, id):
        '''Получение задачи.'''
        for task in self._tasks:
            if str(id) == task.id: return task
        return None

    def update_task(self, id, new_name):
        '''Обновление задачи (имени).'''
        task = self.get_task(id)
        task.name = new_name
        self.storage.dump_tasks(self._tasks)

        return task

    def delete_task(self, id):
        '''Удаление задачи.'''
        for index, task in enumerate(self._tasks):
            if id != task.id:
                continue

            del self._tasks[index]
            self._storage.dump_tasks(self._tasks)

            return task

    @property
    def tasks(self):
        '''Получение всех задач.'''
        return self._tasks
