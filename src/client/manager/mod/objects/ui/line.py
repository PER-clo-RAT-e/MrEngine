from numpy import ceil
import math
from client.manager.mod.objects.ui.base import BaseObject2D, doubleInt


class BaseLine2D(BaseObject2D):
    def __init__(self,
        id: str,
        pos: doubleInt,
        dim: doubleInt,
        rot: int,
    ) -> None:
        super().__init__(id, pos, dim)
        self.rotation = rot

    def _prepare_buffers(self) -> None:
        super()._prepare_buffers()

#       <#=== Braille vBuffer ===#>
        brl_buff = self._brl_buffer

        deg_rot = math.radians(self.rotation)
        rad = self.width/2

        x1, y1 = self.width // 2 + math.sin(deg_rot), self.height // 2 + math.cos(deg_rot)
        x2, y2 = self.width // 2 + math.sin(deg_rot), self.height // 2 + math.cos(deg_rot)

        x_step_am = ceil(x2 - x1)
        y_step_dis = ceil(y2 - y1) / x_step_am

        y = 0
        for x in range(x_step_am):
            y += y_step_dis

            self._brl_buffer[ceil(y), x] = 1


#       <#=== Text vBuffer ===#>
        txt_buff = self._txt_buffer






#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
