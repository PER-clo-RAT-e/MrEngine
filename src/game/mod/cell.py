class Cell:
    def __init__(self, is_mine: bool=False):
        self.is_mine = is_mine
        self.flagged = False
        self.revealed = False
        self.near = 0
        self.neighbors: list[Cell] = []

    def give_neighbors(self, neighbors):
        self.neighbors = neighbors

        for n in self.neighbors:
            if n.is_mine:
                self.near += 1

    def dig(self, recursion_am=0) -> tuple[int, list]:
        dug = 0
        staged = []
        if not self.revealed:
            if self.is_mine:
                return (-1, staged)

            if self.near == 0:
                for n in self.neighbors:
                    if not n.revealed and not n.flagged:
                        if recursion_am > 9:
                            staged.append(n)
                            continue
                        res, st = n.dig(recursion_am + 1)
                        if len(st) > 0:
                            staged.extend(st)
                        if res == -1:
                            return (-1, staged)
                        else:
                            dug += res
            else:
                flagged = 0
                for n in self.neighbors:
                    if n.flagged:
                        flagged += 1
                if flagged >= self.near:
                    for n in self.neighbors:
                        if not n.revealed and not n.flagged:
                            if recursion_am > 200:
                                staged.append(n)
                                continue
                            res, st = n.dig(recursion_am + 1)
                            if len(st) > 0:
                                staged.extend(st)
                            if res == -1:
                                return (-1, staged)
                            else:
                                dug += res

            self.revealed = True

        return (dug, staged)




    def flag(self):
        if not self.revealed:
            self.flagged = not self.flagged

    def __str__(self) -> str:
        if self.flagged:
            return "!"
        elif self.revealed:
            if self.is_mine:
                return "#"
            elif self.near > 0:
                return str(self.near)
            else:
                return " "

        return "."
