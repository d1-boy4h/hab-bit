from ..constants import Navigation

class Router:
    '''Маршрутизатор приложения.'''
    def __init__(self):
        self.current_route: Navigation = Navigation.CALENDAR

    def navigate(self, route: Navigation):
        '''Переключение фокуса на указанный маршрут.'''
        self.current_route = route
