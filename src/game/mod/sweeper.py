from random import uniform
from game.mod.cell import Cell
from game.mod.texty import Texty
from blessed import Terminal
import time


class FieldPointer:
    def __init__(self, limits) -> None:
        self.pos = [0,0]
        self.state = 0
        self.states = ['[]', '{}', '()']
        self.limits = limits

    def get_state(self):
        return self.states[self.state]

    def get_pos(self) -> list[int]:
        return self.pos

    def move(self, dx: int=0, dy: int=0):
        self.pos[0] = min(self.limits[0] - 1, max(0, self.pos[0] + dx))
        self.pos[1] = min(self.limits[1] - 1, max(0, self.pos[1] + dy))


class Field:
    def __init__(self, dimensions: list[int]=[23, 23], mines: int=100):
        print("\033[2J\033[1;1H> Welkome!", end="")
        self.width, self.height = dimensions
        self.mines = mines
        self.field = [[Cell() for _ in range(self.width)] for _ in range(self.height)]
        self.pointer = FieldPointer(dimensions)
        self.term = Terminal()
        self.state = "playing"
        self.is_paused = False
        self.request_restart = False
        self.empty_cells = self.width * self.height - self.mines
        self.run = True

    def update_field(self, x: int, y: int):
        print(self.term.move_xy(x, y) + f" {self.field[y][x]} ", end='')

    def spawn(self):
        amount = self.mines
        probability = self.mines / (self.width * self.height)
        while amount > 0:
            for y in range(self.height):
                for x in range(self.width):
                    if uniform(0, 1) <= probability and not (cell := self.field[y][x]).is_mine and x != 0 and y != 0:
                        cell.is_mine = True

                        amount -= 1

                    if amount == 0:
                        break


        for y in range(self.height):
            for x in range(self.width):
                cell = self.field[y][x]
                neighbors = []
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if dx == 0 and dy == 0:
                            continue

                        nx, ny = x + dx, y + dy

                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            neighbors.append(self.field[ny][nx])

                cell.give_neighbors(neighbors)


    def listen(self):
        texty = Texty()
        term = self.term
        with term.cbreak(), term.hidden_cursor():
            start_t = time.time()
            print(term.home)
            self.draw()
            while self.run:
                print(term.home + f" {round(time.time() - start_t)}s | {self.empty_cells} | Arrows to move; Q to quit; F to flag; D to dig.")
                if self.request_restart:
                    self.field.clear()
                    self.field = [[Cell() for _ in range(self.width)] for _ in range(self.height)]
                    self.spawn()
                    de_pos = self.pointer.get_pos()
                    self.pointer.move(-de_pos[0], -de_pos[1])
                    self.pointer.move()
                    self.request_restart = False
                    self.state = 'playing'
                    start_t = time.time()
                pos_x, pos_y = self.pointer.get_pos()
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

                match key.lower():
                    case "q":
                        self.run = False
                    case "f":
                        self.field[pos_y][pos_x].flag()
                    case "d":
                        result = self.field[pos_y][pos_x].dig()
                        print(term.home + term.move_down(40) + str(result))
                        if result == -1:
                            self.state = "lost"
                        else:
                            self.empty_cells -= result
                            if self.empty_cells == 0:
                                self.state = "victory"
                    case "y":
                        if self.state in ["lost", "victory"]:
                            self.request_restart = True
                    case "c":
                        if self.state == "lost":
                            self.state = "playing"

                match key.name:
                    case "KEY_LEFT":
                        self.pointer.move(-1)
                    case "KEY_RIGHT":
                        self.pointer.move(1)
                    case "KEY_UP":
                        self.pointer.move(0, -1)
                    case "KEY_DOWN":
                        self.pointer.move(0, 1)
                    case "KEY_ESCAPE":
                        self.is_paused = not self.is_paused


    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                color = self.term.normal
                if not (cell := self.field[y][x]).hidden:
                    if cell.is_mine:
                        color = self.term.webmaroon
                    else:
                        match cell.near:
                            case 1:
                                color = self.term.cyan
                            case 2:
                                color = self.term.green
                            case 3:
                                color = self.term.lime
                            case 4:
                                color = self.term.yellow
                            case 5:
                                color = self.term.indianred
                            case 6:
                                color = self.term.orangered
                            case 7:
                                color = self.term.red
                            case 8:
                                color = self.term.brown
                            case _:
                                color = self.term.normal

                if not cell.revealed or cell.flagged:
                    color = self.term.normal

                print(color + f" {cell} ", end='')
            print()
