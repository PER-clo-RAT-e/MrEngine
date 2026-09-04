from threading import Thread
from game.mod.sweeper import Field
from blessed import Terminal
from math import floor
from random import uniform

def main():
    try:
        term = Terminal()
        with term.cbreak(), term.hidden_cursor():
            ready = False
            dimensions = [40, 40, 10]
            mines = 220
            percent = 20
            x_max = 55
            y_max = 45
            z_max = 10
            help_requested = False
            digmode = 0
            digmodes = ["Fast", "Medium", "Slow"]
            while not ready:
                print(term.home + term.clear + term.center("Press Q to exit and H for help.") + term.home + term.move_down(term.height // 2 - 6))
                if help_requested:
                    print(term.center("HELP PAGE"))
                    print("\n\n\n")
                    print(term.center("       H   —  Call this Menu              "))
                    print(term.center("       Q   —  Quit MrSweep.               "))
                    print(term.center("       I   —  Debug Mode.                 "))
                    print(term.center("     ↓↑/←→ —  Move cursor along the borad."))
                    print(term.center("Shift + ↓↑ —  Change the Layer.           "))
                else:

                    print("             ┌ Width ─┐")
                    print(f"      ←/→    │{dimensions[0]:^8}│")
                    print("             └────────┘")

                    print("             ┌ Height ┐")
                    print(f"      ↓/↑    │{dimensions[1]:^8}│")
                    print("             └────────┘")

                    print("             ┌ Mines ─┐")
                    print(f"      -/=    │{mines:^8}│")
                    print("             └────────┘")

                    print("             ┌ Layers ┐")
                    print(f"    Sh↑/Sh↓  │{dimensions[2]:^8}│")
                    print("             └────────┘")

                    print("             ┌ DigMod ┐")
                    print(f"       M     │{digmodes[digmode]:^8}│")
                    print("             └────────┘")

                    probability = mines / (dimensions[0] * dimensions[1])

                    mine_array = [[('#' if uniform(0, 1) < probability else ' ') for _ in range(dimensions[0])] for _ in range(dimensions[1])]

                    print(term.home + term.move_down(term.height//2 - dimensions[1]//2))
                    pr_offs = (term.width - dimensions[0]*2) // 2 - 10
                    x_offset = term.move_right(pr_offs)

                    print(x_offset + f"┌{'———'*(dimensions[0]-2)}┐")

                    for y in range(min(dimensions[1], 40)):
                        print(x_offset + '│', end='')
                        for x in range(dimensions[0]-2):
                            print(f" {mine_array[y][x]} ", end='')
                        print('│')

                    print(x_offset + f"└{'———'*(dimensions[0]-2)}┘")


                key = term.inkey()

                match key.name:
                    case "KEY_LEFT":
                        dimensions[0] = min(x_max, max(20, dimensions[0] - 1))
                    case "KEY_RIGHT":
                        dimensions[0] = min(x_max, max(20, dimensions[0] + 1))
                    case "KEY_UP":
                        dimensions[1] = min(y_max, max(20, dimensions[1] + 1))
                    case "KEY_DOWN":
                        dimensions[1] = min(y_max, max(20, dimensions[1] - 1))
                    case "KEY_SHIFT_UP":
                        dimensions[2] = min(z_max, max(1, dimensions[2] + 1))
                    case "KEY_SHIFT_DOWN":
                        dimensions[2] = min(z_max, max(1, dimensions[2] - 1))
                    case "KEY_ENTER":
                        ready = True


                mines = max(10, min(floor(dimensions[0] * dimensions[1] * percent // 100), mines))

                match key.lower():
                    case "h":
                        help_requested = not help_requested
                    case "=":
                        mines = max(10 * dimensions[2], min(floor(dimensions[0] * dimensions[1] * dimensions[2] * percent // 100), mines + 1))
                    case "-":
                        mines = max(10 * dimensions[2], min(floor(dimensions[0] * dimensions[1] * dimensions[2] * percent // 100), mines - 1))
                    case "m":
                        digmode = 0 if digmode >= 2 else digmode + 1
                    case "q":
                        print("Exiting!")
                        return



        field = Field(dimensions, mines, digmode)

        field.spawn()
        print("Starting the game")
        listen_thread = Thread(target=field.listen)
        listen_thread.start()
        field.render()
    except KeyboardInterrupt:
        print("I'm afraid of Ctrl+C!")


if __name__ == "__main__":
    main()
