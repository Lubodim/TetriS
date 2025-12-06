from typing import List, Tuple, Optional

import pygame

from config import Config, Tetromino, GRAY, BLACK


class Board:

    def __init__(self, config: Config):
        self.config = config
        self.cols = config.cols
        self.rows = config.rows
        self.grid: List[List[Optional[Tuple[int, int, int]]]] = [
            [None for _ in range(self.cols)] for _ in range(self.rows)
        ]
        self.game_over: bool = False

    def is_inside(self, x: int, y: int) -> bool:
        return 0 <= x < self.cols and y < self.rows

    def is_valid_position(
        self,
        tetromino: Tetromino,
        dx: int = 0,
        dy: int = 0,
        rotated: bool = False,
    ) -> bool:

        piece = tetromino.rotated() if rotated else tetromino
        for bx, by in piece.blocks:
            x = piece.x + dx + bx
            y = piece.y + dy + by

            if y < 0:
                continue

            if not self.is_inside(x, y):
                return False

            if self.grid[y][x] is not None:
                return False

        return True

    def lock_tetromino(self, tetromino: Tetromino) -> None:

        for bx, by in tetromino.blocks:
            x = tetromino.x + bx
            y = tetromino.y + by

            if y < 0:
                self.game_over = True
                continue

            if self.is_inside(x, y):
                self.grid[y][x] = tetromino.color

    def clear_full_lines(self) -> int:

        new_grid = [row for row in self.grid if any(cell is None for cell in row)]
        cleared_lines = self.rows - len(new_grid)

        while len(new_grid) < self.rows:
            new_grid.insert(0, [None for _ in range(self.cols)])

        self.grid = new_grid
        return cleared_lines

    def draw(self, surface: pygame.Surface) -> None:
        tile = self.config.tile_size

        for y in range(self.rows):
            for x in range(self.cols):
                rect = pygame.Rect(x * tile, y * tile, tile, tile)
                pygame.draw.rect(surface, GRAY, rect, 0)
                pygame.draw.rect(surface, BLACK, rect, 1)

                color = self.grid[y][x]
                if color is not None:
                    inner_rect = rect.inflate(-4, -4)
                    pygame.draw.rect(surface, color, inner_rect)
