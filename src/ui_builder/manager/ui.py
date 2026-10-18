from dataclasses import dataclass
from collections import deque

@dataclass
class BaseUIObject2DForTOML:
    position: str


class UIManager:
    def __init__(self) -> None:
        self.run = True
        self.elements = deque([])

        self.current_object =
