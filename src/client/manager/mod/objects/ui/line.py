from client.manager.mod.objects.ui.base import BaseObject2D, doubleInt


class BaseLine2D(BaseObject2D):
    def __init__(self,
        id: str,
        pos: doubleInt,
        dimensions: doubleInt,
    ) -> None:
        super().__init__(id, pos, dimensions)
