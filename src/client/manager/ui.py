import tomllib
from pathlib import Path
from enum import StrEnum, auto

from client.manager.event import EventManager
from client.manager.mod.manager import BaseManager


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

    def construct_from_file(self, path: Path):
        with open(path, 'rb') as f:
            data = tomllib.load(f)

        for element in data['components']:
            match element['type']:
                case 'button':
                    pass
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
