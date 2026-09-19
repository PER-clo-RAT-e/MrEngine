from collections import deque
from typing import Optional
from dataclasses import dataclass
import numpy as np

class FieldCursor:
    def __init__(self) -> None:
        self._pos = (0, 0, 0)

    def get_pos(self):
        return self._pos

class FieldManager:
    def __init__(self, dimensions: tuple[int, int, int]) -> None:
        self._dimensions = dimensions
        self._field = np.zeros([*dimensions, 3], dtype=bool)
        self._cursor = FieldCursor()
        self._queue = deque([])

    @property
    def cursor_position(self) -> tuple[int, int, int]:
        return self._cursor.get_pos()


    def flag(self):
        self._field
