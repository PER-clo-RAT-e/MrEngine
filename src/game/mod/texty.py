class Texty:
    def __init__(self) -> None:
        self.game_paused_arr = [
        "    .oooooo.                                                       ",
        "   d8P'  `Y8b                                                      ",
        "  888            .oooo.   ooo. .oo.  .oo.    .ooooo.               ",
        "  888           `P  )88b  `888P\"Y88bP\"Y88b  d88' `88b              ",
        "  888     ooooo  .oP\"888   888   888   888  888ooo888              ",
        "  `88.    .88'  d8(  888   888   888   888  888    .o              ",
        "   `Y8bood8P'   `Y888""8o   o888o o888o o888o `Y8bod8P'            ",
        " ",
        " ",
        "  ooooooooo.                                                  .o8 ",
        "  `888   `Y88.                                               \"888 ",
        "   888   .d88'  .oooo.   oooo  oooo   .oooo.o  .ooooo.   .oooo888 ",
        "   888ooo88P'  `P  )88b  `888  `888  d88(  \"8 d88' `88b d88' `888 ",
        "   888          .oP\"888   888   888  `\"Y88b.  888ooo888 888   888 ",
        "   888         d8(  888   888   888  o.  )88b 888    .o 888   888 ",
        "  o888o        `Y888""8o  `V88V\"V8P' 8""888P' `Y8bod8P' `Y8bod88P\"",
        "                                                                   ",
        "                        Press Esc to start                         "
    ]

        self.game_over_arr =[
    "           .oooooo.                                                    ",
    "          d8P'  `Y8b                                                   ",
    "         888            .oooo.   ooo. .oo.  .oo.    .ooooo.            ",
    "         888           `P  )88b  `888P\"Y88bP\"Y88b  d88' `88b           ",
    "         888     ooooo  .oP\"888   888   888   888  888ooo888           ",
    "         `88.    .88'  d8(  888   888   888   888  888    .o           ",
    "          `Y8bood8P'   `Y888""8o   o888o o888o o888o `Y8bod8P'         ",
    "                                                                       ",
    "                                                                       ",
    "                                                                       ",
    "               .oooooo.                                                ",
    "              d8P'  `Y8b                                               ",
    "             888      888 oooo    ooo  .ooooo.  oooo d8b               ",
    "             888      888  `88.  .8'  d88' `88b `888""8P               ",
    "             888      888   `88..8'   888ooo888  888                   ",
    "             `88b    d88'    `888'    888    .o  888                   ",
    "              `Y8bood8P'      `8'     `Y8bod8P' d888b                  ",
    ]

        self.victory_arr = [
    "   oooooo     oooo  o8o                .                                  .o.    ",
    "    `888.     .8'   `\"'              .o8                                  888    ",
    "     `888.   .8'   oooo   .ooooo.  .o888oo  .ooooo.  oooo d8b oooo    ooo 888    ",
    "      `888. .8'    `888  d88' `\"Y8   888   d88' `88b `888""8P   `88.  .8'  Y8P    ",
    "       `888.8'      888  888         888   888   888  888       `88..8'   `8'    ",
    "        `888'       888  888   .o8   888 . 888   888  888        `888'    .o.    ",
    "         `8'       o888o `Y8bod8P'   \"888\" `Y8bod8P' d888b        .8'     Y8P    ",
    "                                                              .o..P'             ",
    "                                                              `Y8P'              "
        ]

    def get_dim(self, ref):
        return [len(ref), len(ref[0])]
