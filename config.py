from dataclasses import dataclass
from random import random, randint
from typing import List, Tuple


@dataclass(frozen=True)
class Config:
    cols: int = 10
    rows: int = 20
    tile_size: int = 30
    sidebar_width: int = 200
    fps: int = 60

    initial_fall_interval_ms: int = 800
    min_fall_interval_ms: int = 120
    fall_speed_step_ms: int = 60


WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
LIGHT_GRAY = (90, 90, 90)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (50, 205, 50)
BLUE = (65, 105, 225)
CYAN = (0, 206, 209)
YELLOW = (255, 215, 0)
MAGENTA = (186, 85, 211)
ORANGE = (255, 140, 0)




COLORS = [RED, GREEN, BLUE, CYAN, YELLOW, MAGENTA, ORANGE, WHITE, LIGHT_GRAY]



@dataclass
class Tetromino:
    x: int
    y: int
    blocks: List[Tuple[int, int]]
    color: Tuple[int, int, int]

    def rotated(self) -> "Tetromino":

        rotated_blocks = [(-by, bx) for (bx, by) in self.blocks]
        return Tetromino(self.x, self.y, rotated_blocks, self.color)
