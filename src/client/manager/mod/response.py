from typing import Any
from dataclasses import dataclass

from client.manager.mod.state import Status


@dataclass
class BaseManagerResponse:
    status:         Status
    data:           Any|None
