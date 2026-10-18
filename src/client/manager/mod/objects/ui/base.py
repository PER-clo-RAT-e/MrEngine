import numpy as np

type doubleFloat = tuple[float,float]
type doubleInt = tuple[int,int]
type doubleNDArray = tuple[np.ndarray, np.ndarray]
type quadInt = tuple[int,int,int,int]

class BaseObject2D:
    def __init__(self,
        id: str,
        pos: doubleInt,
        dimensions: doubleInt
    ) -> None:

        self.id = id
        self.x  = pos[0]
        self.y  = pos[1]
        self.width = dimensions[0]
        self.height = dimensions[1]

    def _prepare_buffers(self) -> None:
        self._brl_buffer = np.zeros([self.height, self.width])
        self._txt_buffer = np.array([[' ' for _ in range(self.width // 2)] for _ in range(self.height // 4)], dtype=str)

    def _clip_n_copy(self,
        trgt_buff: np.ndarray,
        src_buff: np.ndarray,
        position: doubleFloat
    ) -> None:
        trgt_vb_sy, trgt_vb_sx = trgt_buff.shape
        src_vb_sy, src_vb_sx = src_buff.shape
        h_src_vb_sx, h_src_vb_sy = src_vb_sx // 2, src_vb_sy // 2

        src_vb_px, src_vb_py = int(position[0]), int(position[1])
        src_vb_lft, src_vb_tp = src_vb_px - h_src_vb_sx, src_vb_py - h_src_vb_sy

        trgt_x1, trgt_x2 = max(0, src_vb_lft), min(trgt_vb_sx, src_vb_px + h_src_vb_sx)
        trgt_y1, trgt_y2 = max(0, src_vb_tp), min(trgt_vb_sy, src_vb_py + h_src_vb_sy)

        src_x1, src_x2 = max(0, -src_vb_lft), max(0, -src_vb_lft) + (trgt_x2 - trgt_x1)
        src_y1, src_y2 = max(0, -src_vb_tp), max(0, -src_vb_tp) + (trgt_y2 - trgt_y1)

        if trgt_x1 <= trgt_x2 or trgt_y1 <= trgt_y2:
            trgt_buff[trgt_y1:trgt_y2, trgt_x1:trgt_x2] = src_buff[src_y1:src_y2, src_x1:src_x2]

    def draw(self, csl_vb: np.ndarray, csl_tb: np.ndarray) -> None:
        self._clip_n_copy(csl_vb, self._brl_buffer, (self.x, self.y))

        self._clip_n_copy(csl_tb, self._txt_buffer, (self.x//2, self.y//4))
