from datetime import date as Date, timedelta

class Calendar:
    '''Компонент календаря.'''
    def __init__(self, console, api_client, store, router):
        self._console = console
        self._api_client = api_client
        self._store = store
        self._router = router

    @property
    def _calendar(self):
        return self._get_calendar(self._store.selected_date)

    def _get_calendar(self, current_date: Date) -> list[Date]:
        '''Возвращает массив дней в виде дат текущего месяца.'''
        first_day = Date(current_date.year, current_date.month, 1)
        weekday = first_day.weekday()

        if weekday:
            first_day -= timedelta(days=weekday)

        DAYS_IN_MOUNTH = 42
        return [
            first_day + timedelta(days=d) for d in range(0, DAYS_IN_MOUNTH)
        ]

    def _get_month_word(self, month: int) -> str:
        '''Возвращает текущий месяц в виде слова.'''
        month_list = [
            'Месяц не определён!',
            'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
            'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
        ]

        if 1 <= month <= 12:
            return month_list[month]
        return month_list[0]

    def _render_month_title(self):
        '''Отрисовка текущего месяца.'''
        selected_date = self._store.selected_date
        current_month_word = self._get_month_word(selected_date.month)
        self._console.print(f'Текущий месяц: [bold]{current_month_word}[/]')

    def _render_calendar_grid_title(self):
        '''Отрисовка дней недели над календарной сеткой.'''
        days_of_week = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
        style = 'black on white'
        for weekday in days_of_week:
            self._console.print(f' {weekday} ', end='', style=style)
        else:
            self._console.print()

    def _add_space(self, day: int) -> str:
        '''Добавляет пробел перед числом, если оно однозначное.'''
        return f' {day}' if day < 10 else str(day)

    def _is_day_completed(self, date: Date) -> bool:
        '''Проверка, что все задачи дня выполнены.'''
        tasks = self._api_client.get_tasks_for_day(date)

        if not tasks:
            return True

        day = self._api_client.get_day(date)
        return len(tasks) == len(day.completed_tasks)

    def _get_style_for_day(self, date: Date, today: Date) -> str:
        '''Возвращает стилизацию для календарного дня.'''
        background = ''
        text = ''
        selected = ''

        if date == today:
            # Если день - сегодня
            text = 'white'
            background = 'on blue'
        elif date.month != today.month:
            # Если день не принадлежит текущему месяцу
            text = 'white'
            background = 'on grey19'
        elif date > today:
            # Дни, которые ещё не настали
            text = 'white'
            background = 'on grey42'
        elif self._is_day_completed(date):
            # Полностью выполненный день
            text = 'white'
            background = 'on dark_sea_green4'
        else:
            # Проваленный день
            text = 'white'
            background = 'on red3'

        if date == self._store.selected_date:
            selected = 'u bold'

        return f'{selected} {text} {background}'

    def _render_calendar_grid(self):
        '''Отрисовка календарной сетки.'''
        for day_index, date in enumerate(self._calendar):
            style = self._get_style_for_day(date, Date.today())
            self._console.print(
                f' {self._add_space(date.day)} ',
                end='',
                style=style
            )

            if not (day_index + 1) % 7:
                self._console.print()

    def render(self):
        '''Отрисовка компонента календаря.'''
        self._render_month_title()
        self._render_calendar_grid_title()
        self._render_calendar_grid()
