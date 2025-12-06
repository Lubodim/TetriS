
class Colors:
    WHITE = (255, 255, 255)
    GRAY = (40, 40, 40)
    LIGHT_GRAY = (90, 90, 90)
    DARK_GRAY = (30, 30, 30)
    BLACK = (0, 0, 0)
    RED = (220, 20, 60)
    GREEN = (50, 205, 50)
    BLUE = (65, 105, 225)
    CYAN = (0, 206, 209)
    YELLOW = (255, 215, 0)
    MAGENTA = (186, 85, 211)
    ORANGE = (255, 140, 0)


class Config:
    def __init__(self):
        self.cols = 10
        self.rows = 20
        self.tile_size = 30
        self.sidebar_width = 200
        self.fps = 60

        self.colors = {
            "WHITE": Colors.WHITE,
            "GRAY": Colors.GRAY,
            "DARK_GRAY": Colors.DARK_GRAY,
            "BLACK": Colors.BLACK,
        }
