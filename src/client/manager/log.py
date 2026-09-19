from enum import Enum, auto
from typing import Any
from dataclasses import dataclass

class LogManagerStatus(Enum):
    SUCCESS = auto()
    WARNING = auto()
    ERROR = auto()

@dataclass
class LogManagerResult:
    status: str
    data:           Any|None
    error_message:  str|None

class LogManager:
    def __init__(self) -> None:
        pass
