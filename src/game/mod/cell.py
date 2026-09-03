class Cell:
    def __init__(self, is_mine: bool=False):
        self.is_mine = is_mine
        self.hidden = True
        self.flagged = False
        self.revealed = False
        self.near = 0
        self.neighbors: list[Cell] = []

    def give_neighbors(self, neighbors):
        self.neighbors = neighbors

        for n in self.neighbors:
            if n.is_mine:
                self.near += 1

    def dig(self, revealed=0) -> int:
        result = 0
        if self.hidden or not self.flagged:
            if self.revealed:
                flagged = 0
                for n in self.neighbors:
                    if n.flagged:
                        flagged += 1

                if flagged >= self.near:
                    for n in self.neighbors:
                        if not n.revealed and not n.flagged:
                            n.dig()


            else:
                self.revealed = True
                if self.is_mine:
                    result = -1
                elif self.near == 0:
                    result = 1
                    for n in self.neighbors:
                        if not n.revealed:
                            self.hidden = False
                            res = n.dig(revealed + 1)
                            if res == -1:
                                return -1
                            else:
                                result += res
                else:
                    result = 1


        self.hidden = False
        return result

    def flag(self):
        if not self.revealed:
            self.flagged = not self.flagged
            self.hidden = not self.hidden

            if self.flagged:
                return 1

    def __str__(self) -> str:
        if not self.hidden:
            if self.flagged:
                return "!"
            if self.is_mine:
                return "#"
            elif self.near > 0:
                return str(self.near)
            else:
                return " "

        return "."
