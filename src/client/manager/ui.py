import tomllib
from pathlib import Path
from enum import StrEnum, auto

from client.manager.event import EventManager
from client.manager.mod.manager import BaseManager
from client.manager.mod.objects.ui.button import BaseButton2D
from client.manager.mod.objects.ui.line import BaseLine2D

class FileReader:
    def __init__(self) -> None:
        self.current_sceme = []

    def _parse(self, data: str):            #! TOBE DELETED
        for line in data:
            pass

    def open_sceme(self, path: Path):
        with open(path, 'r') as f:
            data = f.read()


class Menu(StrEnum):
    Main     = auto()
    Settings = auto()
    Game     = auto()

class SettingsSubMenu(StrEnum):
    NoSubMenu     = auto()
    General       = auto()
    Controls      = auto()
    Miscellaneous = auto()

class PopUpMenu(StrEnum):
    NoPopUp      = auto()
    FileExplorer = auto()
    Results      = auto()
    ServerSearch = auto()

class UIManager(BaseManager)
    def __init__(self, event_manger: EventManager) -> None:
        super().__init__()
        self._elements = {}
        self._ids: dict[str, int] = {}

    def construct_from_file(self, path: Path):
        with open(path, 'rb') as f:
            data = tomllib.load(f)

        for element in data['components']:
            el_type = element["type"]
            if el_type not in self._ids:
                self._ids[el_type] = 0
            self._ids[el_type] += 1
            match el_type:
                case 'button':
                    object = BaseButton2D(
                        "Button::" + str(self._ids[el_type]),
                        (0, 0),
                        (40, 30)
                    )
                case 'label':
                    pass
                case 'line':
                    pass
                case 'x-canvas':
                    pass
                case 'y-canvas':
                    pass
                case 'xy-canvas':
                    pass
