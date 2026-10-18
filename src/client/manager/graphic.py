from blessed import Terminal
import time
from threading import Thread
import numpy as np
from dataclasses import dataclass
from client.manager.event import ApplicationEvent, EventManager
from client.manager.mod.manager import BaseManager
from client.manager.mod.objects.ui.button import BaseButton2D
from client.manager.mod.response import BaseManagerResponse
from client.manager.mod.state import BaseError, Status

class GraphicManagerError(BaseError):
    NO_TERM = "Didn't get the terminal variable. Seems like noone initialised it?"
    NO_VBUF = "Didn't get the virtual buffer. Seems like noone initialised it?"

@dataclass
class GraphicManagerResponse(BaseManagerResponse):
    error_message:  GraphicManagerError|None = None

type drawableClass = BaseButton2D

class GraphicManager(BaseManager):
    def __init__(self, event_manager: EventManager) -> None:
        super().__init__()

        self._term = Terminal()
        self._event_manager = event_manager

        self._event_manager.subscribe(ApplicationEvent.TERMINATE,
            lambda: self._state.set_status(Status.SHUTDOWN))

        width, height = self._term.width*2, self._term.height*4

        self._dim = (width, height)

        self._elements: dict[str, dict[str, drawableClass]] = {
            "back": {},
            "front": {},
        }

        self._brl_buffer = np.zeros([int(height), int(width)])
        self._txt_buffer = np.array([[' ' for _ in range(width//2)] for _ in range(height//4)], dtype=str)

        self.WEIGHTS = [
            [ 1,   8],
            [ 2,  16],
            [ 4,  32],
            [64, 128]
        ]

        self._state.set_status(Status.IDLE)

    def demonise(self) -> Thread:
        thread = Thread(target=self._cycle, daemon=True)
        thread.start()

        return thread

    def _braille_to_txt(self, vb: np.ndarray) -> np.ndarray:
        csl_vb_sy, csl_vb_sx = vb.shape

        blckd_vb = vb.reshape(csl_vb_sy // 4, 4, csl_vb_sx //2, 2).swapaxes(1, 2)

        ready_vb_codes = 0x2800 + (blckd_vb * self.WEIGHTS).sum(axis=(-2, -1)).astype(int)

        return np.vectorize(chr)(ready_vb_codes)

    def add_bg_elemnt(self, name: str, element: drawableClass):
        self._elements['back'][name] = element

    def add_fg_elemnt(self, name: str, element: drawableClass):
        self._elements['front'][name] = element


    def _clip_nd_cp_bffrs(self,
        trgt_buff: np.ndarray,
        src_buff: np.ndarray,
    ) -> None:
        trgt_vb_sy, trgt_vb_sx = trgt_buff.shape
        src_vb_sy, src_vb_sx = src_buff.shape
        h_src_vb_sx, h_src_vb_sy = src_vb_sx // 2, src_vb_sy // 2

        src_vb_px, src_vb_py = trgt_vb_sx//2, trgt_vb_sy//2
        src_vb_lft, src_vb_tp = src_vb_px - h_src_vb_sx, src_vb_py - h_src_vb_sy

        trgt_x1, trgt_x2 = max(0, src_vb_lft), min(trgt_vb_sx, src_vb_px + h_src_vb_sx)
        trgt_y1, trgt_y2 = max(0, src_vb_tp), min(trgt_vb_sy, src_vb_py + h_src_vb_sy)

        src_x1, src_x2 = max(0, -src_vb_lft), max(0, -src_vb_lft) + (trgt_x2 - trgt_x1)
        src_y1, src_y2 = max(0, -src_vb_tp), max(0, -src_vb_tp) + (trgt_y2 - trgt_y1)

        if trgt_x1 <= trgt_x2 or trgt_y1 <= trgt_y2:
            trgt_buff[trgt_y1:trgt_y2, trgt_x1:trgt_x2] = src_buff[src_y1:src_y2, src_x1:src_x2]

    def _cycle(self):
        while self.status not in [Status.ATERROR, Status.SHUTDOWN]:

            for element in self._elements['back'].values():
                element.draw(self._brl_buffer, self._txt_buffer)


            for element in self._elements['front'].values():
                element.draw(self._brl_buffer, self._txt_buffer)


            new_txt_buff = self._braille_to_txt(self._brl_buffer)

            mask = self._txt_buffer != ' '
            new_txt_buff[mask] = self._txt_buffer[mask]


            print(self._term.move_xy(0,0) + '\n'.join(''.join(line) for line in new_txt_buff), end='', flush=True)


            time.sleep(0.1)
