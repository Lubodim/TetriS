import random
from typing import List, Tuple
from config import Colors


class Tetromino:
    def __init__(self, x: int, y: int, blocks: List[Tuple[int, int]], color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.blocks = blocks
        self.color = color

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy

    def rotate(self) -> None:
        self.blocks = [(-by, bx) for (bx, by) in self.blocks]

    def get_cells(self) -> List[Tuple[int, int]]:
        return [(self.x + bx, self.y + by) for (bx, by) in self.blocks]

    def can_move_down(self, rows: int) -> bool:
        for _, y in self.get_cells():
            if y + 1 >= rows:
                return False
        return True

    def is_within_bounds(self, cols: int, rows: int) -> bool:
        for x, y in self.get_cells():
            if x < 0 or x >= cols:
                return False
            if y >= rows:
                return False
        return True


class TetroFactory:
    SHAPES = [
        [(0, -1), (0, 0), (0, 1), (0, 2)],
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        [(-1, 0), (0, 0), (1, 0), (0, 1)],
        [(-1, 0), (0, 0), (1, 0), (-1, 1)],
        [(-1, 0), (0, 0), (1, 0), (1, 1)],
        [(-1, 1), (0, 1), (0, 0), (1, 0)],
        [(-1, 0), (0, 0), (0, 1), (1, 1)],
    ]

    COLORS = [
        Colors.RED,
        Colors.GREEN,
        Colors.BLUE,
        Colors.CYAN,
        Colors.YELLOW,
        Colors.MAGENTA,
        Colors.ORANGE,
    ]

    @classmethod
    def create_random(cls, board_cols: int) -> Tetromino:
        shape = random.choice(cls.SHAPES)
        color = random.choice(cls.COLORS)
        start_x = board_cols // 2
        start_y = 0
        return Tetromino(start_x, start_y, shape, color)
