from typing import Callable

class ParserManager:
    def __init__(self) -> None:
        self.endpoints: dict[str, dict[str, Callable]] = {}

    def subscribe(self, parser, name, function):
        pass
