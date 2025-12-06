import random

from config import Tetromino, COLORS


class TetrominoFactory:

    SHAPES = [
        # I-форма
        [(0, -1), (0, 0), (0, 1), (0, 2)],
        # O-форма
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        # T-форма
        [(-1, 0), (0, 0), (1, 0), (0, 1)],
        # L-форма
        [(-1, 0), (0, 0), (1, 0), (-1, 1)],
        # J-форма
        [(-1, 0), (0, 0), (1, 0), (1, 1)],
        # S-форма
        [(-1, 1), (0, 1), (0, 0), (1, 0)],
        # Z-форма
        [(-1, 0), (0, 0), (0, 1), (1, 1)],
    ]

    @classmethod
    def create_random(cls, board_cols: int) -> Tetromino:
        shape = random.choice(cls.SHAPES)
        color = random.choice(COLORS)

        start_x = board_cols // 2
        start_y = -2
        return Tetromino(start_x, start_y, shape, color)


