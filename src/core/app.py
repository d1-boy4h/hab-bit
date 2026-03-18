import logging
from datetime import date

from .store import Store
from .router import Router
from ..api import ApiClient
from ..handlers import KeyboardHandler
from ..ui import Interface

class App:
    '''Ядро программы.'''
    def __init__(self):
        self._api_client = ApiClient()
        self._store = Store()
        self._router = Router()

        self._logger = logging.getLogger('Core')
        self._log_level = logging.INFO

        self._keyboard_handler = KeyboardHandler(
            self._api_client,
            self._store,
            self._router,
        )

        self._interface = Interface(
            self._api_client,
            self._store,
            self._router,
            self._keyboard_handler
        )

    def run(self):
        logging.basicConfig(
            filename=f'logs/{date.today()}.log',
            format='%(asctime)s [%(levelname)s | %(name)s] %(message)s',
            level=self._log_level
        )

        self._logger.info('Запус клиента...')
        self._interface.run()
        self._logger.info('Клиент завершил свою работу')
