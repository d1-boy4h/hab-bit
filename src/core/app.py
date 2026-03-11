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
        self._interface.run()
