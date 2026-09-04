from collections import deque
from ast import type_ignore
from random import uniform
from game.mod.cell import Cell
from game.mod.texty import Texty
from blessed import Terminal
import time


class FieldPointer:
    def __init__(self, limits) -> None:
        self.pos = [0,0,0]
        self.state = 0
        self.states = ['[]', '{}', '()']
        self.limits = limits

    def get_state(self):
        return self.states[self.state]

    def get_pos(self) -> list[int]:
        return self.pos

    def move(self, dx: int=0, dy: int=0, dz: int=0):
        self.pos[0] = min(self.limits[0] - 1, max(0, self.pos[0] + dx))
        self.pos[1] = min(self.limits[1] - 1, max(0, self.pos[1] + dy))
        self.pos[2] = min(self.limits[2] - 1, max(0, self.pos[2] + dz))


class Field:
    def __init__(self, dimensions: list[int]=[23, 23, 1], mines: int=100):
        print("\033[2J\033[1;1H> Welkome!", end="")
        self.width, self.height, self.depth = dimensions
        self.ratios = self.get_ratios()
        self.mines = mines
        self.field = [
            [
                [Cell() for _ in range(self.width)]
                for _ in range(self.height)]
            for _ in range(self.depth)
        ]
        self.busy = False
        self.pointer = FieldPointer(dimensions)
        self.term = Terminal()
        self.state = "playing"
        self.is_paused = False
        self.request_restart = False
        self.colors = [self.term.cyan, self.term.green, self.term.lime, self.term.yellow, self.term.indianred, self.term.orangered, self.term.red, self.term.brown]
        self.empty_cells = self.width * self.height * self.depth - self.mines
        self.dug = 0
        self.info_requested = False
        self.key = None
        self.run = True

    def update_field(self, x: int, y: int, z: int):
        print(self.term.move_xy(x, y) + f" {self.field[z][y][x]} ", end='')

    def get_ratios(self):
        s = [self.width, self.height, self.depth]
        s.sort()

        match s:
            case [self.width, self.height, self.depth]:#        x | y | z
                return (1, s[1]//s[0], s[2]//s[0])
            case [self.width, self.depth, self.height]:#        x | z | y
                return (1, s[2]//s[0], s[1]//s[0])
            case [self.height, self.width, self.depth]:#        y | x | z
                return (s[1]//s[0], 1, s[2]//s[0])
            case [self.height, self.depth, self.width]:#        y | z | x
                return (s[1]//s[0], s[2]//s[0], 1)
            case [self.depth, self.height, self.width]:#        z | y | x
                return (s[2]//s[0], s[1]//s[0], 1)
            case [self.height, self.depth, self.width]:#        3 | x | z
                return (s[2]//s[0], 1, s[1]//s[0])

    def spawn(self):
        amount = self.mines
        probability = self.mines / (self.width * self.height)
        while amount > 0:
            for z in range(self.depth):
                for y in range(self.height):
                    for x in range(self.width):
                        if uniform(0, 1) <= probability and not (cell := self.field[z][y][x]).is_mine and (x != 0 and y != 0 and z!=1):
                            cell.is_mine = True

                            amount -= 1

                        if amount == 0:
                            break
                    if amount == 0:
                        break
                if amount == 0:
                    break


        for z in range(self.depth):
            for y in range(self.height):
                for x in range(self.width):
                    cell = self.field[z][y][x]
                    neighbors = []
                    for dz in range(-1, 2):
                        for dy in range(-1, 2):
                            for dx in range(-1, 2):
                                if dx == 0 and dy == 0 and dz == 0:
                                    continue

                                nx, ny, nz = x + dx, y + dy, z + dz

                                if 0 <= nx < self.width and 0 <= ny < self.height and 0 <= nz < self.depth:
                                    neighbors.append(self.field[nz][ny][nx])

                    cell.give_neighbors(neighbors)



    def listen(self):
        texty = Texty()
        term = self.term
        with term.cbreak(), term.hidden_cursor():
            start_t = time.time()
            print(term.home)
            self.draw()
            while self.run:
                print(term.home + f" {round(time.time() - start_t)}s | {self.empty_cells} | Arrows to move (Shift for layers); Q to quit; F to flag; D to dig.")
                if self.request_restart:
                    self.field.clear()
                    self.field = [
                        [
                            [Cell() for _ in range(self.width)]
                            for _ in range(self.height)]
                        for _ in range(self.depth)
                    ]
                    self.spawn()
                    de_pos = self.pointer.get_pos()
                    self.pointer.move(-de_pos[0], -de_pos[1])
                    self.pointer.move()
                    self.request_restart = False
                    self.state = 'playing'
                    start_t = time.time()
                pos_x, pos_y, pos_z = self.pointer.get_pos()
                state = self.pointer.get_state()


                if self.state == "lost":
                    start_y = term.height // 2 - texty.get_dim(texty.game_paused_arr)[0]
                    print(term.home + term.clear + term.move_xy(0, start_y) + '\n'.join(texty.game_over_arr))
                    print("\n  Press Y to restart; C to continue, Q to quit")

                elif self.state == "victory":
                    start_y = term.height // 2 - texty.get_dim(texty.victory_arr)[0]
                    print(term.home + term.clear + term.move_xy(0, start_y) + '\n'.join(texty.victory_arr))
                    print("\n  Press Y to restart; Q to quit")
                else:
                    print(term.home)
                    self.draw()

                    print(term.move_xy(pos_x * 3, pos_y + 1) + state[0])
                    print(term.move_xy(pos_x * 3 + 2, pos_y + 1) + state[1])



                key = term.inkey()
                self.key = key

                match key.lower():
                    case "q":
                        self.run = False
                    case "f":
                        self.field[pos_z][pos_y][pos_x].flag()
                    case "d":
                        staged = deque([self.field[pos_z][pos_y][pos_x]])
                        dug = 0
                        self.busy = True
                        while len(staged) != 0:
                            dg, st = staged[0].dig()
                            staged.popleft()

                            dug += dg
                            staged.extend(st)

                        self.dug = dug

                        self.busy = False
                        if dug == -1:
                            self.state = "lost"
                        else:
                            self.empty_cells -= dug
                            if self.empty_cells == 0:
                                self.state = "victory"
                    case "y":
                        if self.state in ["lost", "victory"]:
                            self.request_restart = True
                    case "c":
                        if self.state == "lost":
                            self.state = "playing"
                        print(term.clear)
                    case "i":
                        self.info_requested = not self.info_requested
                        print(term.clear)

                match key.name:
                    case "KEY_LEFT":
                        self.pointer.move(-1)
                    case "KEY_RIGHT":
                        self.pointer.move(1)
                    case "KEY_UP":
                        self.pointer.move(0, -1)
                    case "KEY_DOWN":
                        self.pointer.move(0, 1)
                    case "KEY_SHIFT_UP":
                        self.pointer.move(0, 0, 1)
                    case "KEY_SHIFT_DOWN":
                        self.pointer.move(0, 0, -1)
                    case "KEY_ESCAPE":
                        self.is_paused = not self.is_paused


    def draw(self):
        cur_x, cur_y, cur_z = self.pointer.get_pos()
        for y in range(self.height):
            for x in range(self.width):
                color = self.term.normal
                if not (cell := self.field[cur_z][y][x]).revealed:
                    if cell.is_mine:
                        color = self.term.webmaroon
                    elif self.depth > 1:
                        color = self.colors[min(8, max(0, cell.near//3))]
                    else:
                        color = self.colors[cell.near]

                if not cell.revealed or cell.flagged:
                    color = self.term.normal

                print(color + f" {cell} ", end='')
            print()

        if self.info_requested:
            cell = self.field[cur_z][cur_y][cur_x]
            print(self.term.move_xy(168, 3) + f"Is Mine: {int(cell.is_mine)}")
            print(self.term.move_right(168) + f"Flagged: {int(cell.flagged)}")
            print(self.term.move_right(168) + f"Pos: {cur_x}:{cur_y}:{cur_z}")
            print(self.term.move_right(168) + f"Mine Sum: {sum([c.is_mine for c in cell.neighbors])}")
            print(self.term.move_right(168) + f"Near Mines: {cell.near}")
            print(self.term.move_right(168) + f"Flag Sum: {sum([int(c.flagged) for c in cell.neighbors])}")

            print(self.term.move_down(1) + self.term.move_right(168) + f"Key Pressed: {self.key.name if self.key is not None else self.key}             ")
            print(self.term.move_right(168) + f"Is Busy: {self.busy}")

            print(self.term.move_down(1) + self.term.move_right(168) + f"Dug: {self.dug}            ")
            print(self.term.move_right(168) + f"Dimensions: {self.width}::{self.height}::{self.depth}")

        for _depth in range(self.depth):
            if _depth == cur_z:
                level = "#"
            else:
                level = "—"
            print(self.term.home + self.term.move_xy(self.term.width - 4, 3 + self.depth - _depth) + level)
