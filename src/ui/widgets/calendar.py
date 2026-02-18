from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import Grid
from textual.widgets import Static, Button

class CalendarWidget(Widget):
    '''Виджет календаря.'''
    def __init__(self, days_manager, tasks_widget_ref):
        self._days_manager = days_manager
        self._tasks_widget_ref = tasks_widget_ref

        super().__init__()

    def compose(self) -> ComposeResult:
        yield Static(id='calendar-title', classes='title')

        days_of_week = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
        with Grid(classes='weekdays'):
            for weekday in days_of_week:
                yield Static(weekday, classes='weekday')

        yield Grid(id='calendar', classes='calendar')

    def build(self):
        '''Рендер виджета.'''
        title = self.query_one('#calendar-title')
        title.update(f'Текущий месяц: {self._get_month_word(self._days_manager.month)}')

        calendar_container = self.query_one('#calendar')
        calendar_container.remove_children()

        for day in self._days_manager.calendar:
            calendar_container.mount(Button(
                str(day.date.day),
                id=f'day-{str(day.date)}-{self._days_manager.get_id()}',
                classes=self._get_classes_for_day(day, self._days_manager.today)
            ))

    def on_mount(self):
        self.build()

    def _get_classes_for_day(self, day, today):
        base_class = 'day_btn'

        additional_class = ''
        if day.date == today:
            additional_class = 'today'
        elif day.date.month != today.month:
            additional_class = 'another'
        elif day.date > today:
            additional_class = 'future'
        elif self._days_manager.is_day_completed(day):
            additional_class = 'completed'
        else:
            additional_class = 'failed'

        if day.date == self._days_manager.selected_date:
            additional_class = additional_class + ' ' + 'selected'

        return f'{base_class} {additional_class}'

    def _get_month_word(self, month: int) -> str:
        '''Возвращает текущий месяц в виде слова.'''
        month_list = [
            'Месяц не определён!',
            'Январь',
            'Февраль',
            'Март',
            'Апрель',
            'Май',
            'Июнь',
            'Июль',
            'Август',
            'Сентябрь',
            'Октябрь',
            'Ноябрь',
            'Декабрь'
        ]

        if month > 0 or month <= 12:
            return month_list[month] 
        else:
            return month_list[0]

    def on_button_pressed(self, event: Button.Pressed):
        date_str = event.button.id.partition('-')[-1].rpartition('-')[0]
        self._days_manager.change_selected_date(date_str)
        self.build()
        self._tasks_widget_ref.build()
