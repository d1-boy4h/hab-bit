class Header:
    '''Компонент шапки приложения.'''
    def __init__(self, console):
        self._console = console

    def render(self):
        '''Отрисовка компонента шапки.'''
        title = '📅 hab-bit - календарь полезных привычек ⚡️'
        style = 'white on grey35'

        self._console.print(title, style=style, justify='center')
