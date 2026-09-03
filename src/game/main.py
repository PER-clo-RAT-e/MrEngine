from game.mod.sweeper import Field
from blessed import Terminal
from math import floor
from random import uniform

def main():
    try:
        term = Terminal()
        with term.cbreak(), term.hidden_cursor():
            ready = False
            dimensions = [40, 40]
            mines = 220
            percent = 20
            x_max = 55
            y_max = 45
            while not ready:
                print(term.home + term.clear + "Press Arrows to change dimensions; -/= for amount of mines.\n")
                print("┌─ Width ┐")
                print(f"│{dimensions[0]:^8}│")
                print("└────────┘")
                print(term.home + term.move_down(2) + term.move_right(10) + "┌ Height ┐")
                print(term.move_right(10) + f"│{dimensions[1]:^8}│")
                print(term.move_right(10) + "└────────┘")
                print(term.home + term.move_down(2) + term.move_right(20) + f"┌ Mines ─┐")
                print(term.move_right(20) + f"│{mines:^8}│")
                print(term.move_right(20) + "└────────┘")

                probability = mines / (dimensions[0] * dimensions[1])

                mine_array = [[('#' if uniform(0, 1) < probability else ' ') for _ in range(dimensions[0])] for _ in range(dimensions[1])]

                print(f"┌{'———'*(dimensions[0]-2)}┐" + '   '*(x_max - dimensions[0]+2))

                for y in range(min(dimensions[1], 40)):
                    print('│', end='')
                    for x in range(dimensions[0]-2):
                        print(f" {mine_array[y][x]} ", end='')
                    print('│')

                print(f"└{'———'*(dimensions[0]-2)}┘" + '   '*(x_max - dimensions[0]+2))

                key = term.inkey()

                match key.name:
                    case "KEY_LEFT":
                        dimensions[0] = min(x_max, max(20, dimensions[0] - 1))
                    case "KEY_RIGHT":
                        dimensions[0] = min(x_max, max(20, dimensions[0] + 1))
                    case "KEY_UP":
                        dimensions[1] = min(y_max, max(20, dimensions[1] - 1))
                    case "KEY_DOWN":
                        dimensions[1] = min(y_max, max(20, dimensions[1] + 1))
                    case "KEY_ENTER":
                        ready = True


                mines = max(10, min(floor(dimensions[0] * dimensions[1] * percent // 100), mines))

                match key.lower():
                    case "=":
                        mines = max(10, min(floor(dimensions[0] * dimensions[1] * percent // 100), mines + 1))
                    case "-":
                        mines = max(10, min(floor(dimensions[0] * dimensions[1] * percent // 100), mines - 1))
                    case "q":
                        print("Exiting!")
                        return


        field = Field(dimensions, mines)

        field.spawn()
        field.listen()
    except KeyboardInterrupt:
        print("I'm afraid of Ctrl+C!")


if __name__ == "__main__":
    main()
