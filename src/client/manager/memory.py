from typing import Any
from enum import Enum, auto
from dataclasses import dataclass

from client.manager.mod.state import BaseError

class MemoriserStatus(Enum):
    SUCCESS = auto()
    WARNING = auto()
    ERROR   = auto()


class MemoriserError(BaseError):
    NOT_FOUND = "Object {} is not found."


@dataclass
class MemoriserResponse:
    status:         MemoriserStatus
    data:           Any|None =      None
    error_message:  str|None =      None

class Memoriser:
    def __init__(self) -> None:
        self.mem: dict[str, Any] = {".env": {}}


    def get(self, element_name: str, is_in_env=False) -> MemoriserResponse:
        if is_in_env:
            element = self.mem['.env'].get(element_name, MemoriserStatus.ERROR)
        else:
            element = self.mem.get(element_name, MemoriserStatus.ERROR)


        if element == MemoriserStatus.ERROR:
            return MemoriserResponse(
                element,
                None,
                MemoriserError.NOT_FOUND[1:].format(element_name)
            )

        else:
            return MemoriserResponse(
                MemoriserStatus.SUCCESS,
                element
            )

    def add(self, name, element):
        self.mem[name] = element
