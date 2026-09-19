from enum import StrEnum, auto
from typing import Callable

class ApplicationEvent(StrEnum):
    TERMINATE = auto()

class EventManager:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable]] = {}

    def subscribe(self, event: str, callback: Callable):
        if event not in self._subscribers:
            self._subscribers[event] = []

        self._subscribers[event].append(callback)

    def _dummy(self, *args, **kwargs):
        pass

    def emit(self, event: str, *args, **kwargs):
        for func in self._subscribers.get(event, [self._dummy]):
            func(*args, **kwargs)
