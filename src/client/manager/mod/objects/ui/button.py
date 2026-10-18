import numpy as np

from client.manager.mod.objects.ui.base import BaseObject2D, doubleInt, quadInt


class BaseButton2D(BaseObject2D):
    def __init__(self,
        id: str,
        pos: doubleInt,
        dimensions: doubleInt,
        border: quadInt=(0,2,4,6),
        text: str="Button"
    ) -> None:
        super().__init__(id, pos, dimensions)
        self.text = text
        self.border = border
        self._prepare_buffers()


    def _prepare_buffers(self) -> None:
        def separate_text(text:str, max_width:int, max_height: int) -> list[list[str]]:
            sep_wrds = [[]]
            max_w = 0
            size = 0
            line = 0
            for word in text.split(" "):
                size += 1
                if size + len(word) >= max_width:
                    if len(word) > max_width:
                        word = word[:max_width]
                    sep_wrds.append([])
                    line += 1
                    if size > max_w:
                        max_w = size
                    size = 0
                size += len(word)

                sep_wrds[line].append(word)

            return [list(f"{' '.join(line):^{max_width}}") for line in sep_wrds][:max_height]

#       ! Welkome to Purgatory.
#       <#=== Braille vBuffer ===#>
        super()._prepare_buffers()

        brl_buff = self._brl_buffer
        btn_brdr_s_tp, btn_brdr_s_rght, btn_brdr_s_btm, btn_brdr_s_lft = self.border

        brl_buff[0:btn_brdr_s_tp, :] = 1
        brl_buff[:, -btn_brdr_s_rght:] = 1
        brl_buff[-btn_brdr_s_btm:, :] = 1
        brl_buff[:, 0:btn_brdr_s_lft] = 1


#       <#=== Text vBuffer ===#>
        txt_buff = self._txt_buffer
        txt_buff_sy, txt_buff_sx = txt_buff.shape

        fr_spc_sx = txt_buff_sx - btn_brdr_s_lft//2 - btn_brdr_s_rght//2
        fr_spc_sy = txt_buff_sy - btn_brdr_s_tp//4 - btn_brdr_s_btm//4
        #self.text = str(fr_spc_sx)

        with open('out/log.txt', 'w') as f:
            f.write(f"{fr_spc_sx}:{fr_spc_sy}")


        tmp = np.array(separate_text(self.text, fr_spc_sx, fr_spc_sy), dtype=str)

        self._clip_n_copy(self._txt_buffer, tmp, (txt_buff_sx//2, txt_buff_sy//2))
