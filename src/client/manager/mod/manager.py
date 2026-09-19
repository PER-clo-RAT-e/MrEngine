from client.manager.memory import Memoriser
from client.manager.mod.state import ManagerState


class BaseManager:
    def __init__(self) -> None:
        self._state = ManagerState()

    @property
    def status(self):
        return self._state.status

    @property
    def err_reason(self):
        return self._state.error
