from collections import deque
from enum import Enum, auto, StrEnum
from dataclasses import dataclass

class Status(Enum):
    STARTUP  = auto()
    IDLE     = auto()
    BUSY     = auto()
    ATERROR  = auto()
    SHUTDOWN = auto()

class BaseError(StrEnum):
    pass

@dataclass
class ManagerState:
    def __init__(self) -> None:
        self.status = Status.STARTUP
        self.error_list: deque[BaseError] = deque([])

    def error(self, error: BaseError):
        self.status = Status.ATERROR
        self.error_list.append(error)

    def set_status(self, status: Status):
        self.status = status
