from typing import List, Optional, Tuple
import pygame
import random


from config import Config, Colors


class Board:
    def __init__(self, config: Config):
        self.config = config
        self.cols = config.cols
        self.rows = config.rows
        self.grid: List[List[Optional[Tuple[int, int, int]]]] = [
            [None for _ in range(self.cols)] for _ in range(self.rows)
        ]

    def draw(self, screen: pygame.Surface) -> None:
        tile = self.config.tile_size
        for y in range(self.rows):
            for x in range(self.cols):
                rect = pygame.Rect(x * tile, y * tile, tile, tile)
                pygame.draw.rect(screen, Colors.GRAY, rect)
                pygame.draw.rect(screen, Colors.BLACK, rect, 1)
                cell_color = self.grid[y][x]
                if cell_color is not None:
                    inner = rect.inflate(-4, -4)
                    pygame.draw.rect(screen, cell_color, inner)

    def is_valid_position(self, tetromino) -> bool:
        for x, y in tetromino.get_cells():
            if x < 0 or x >= self.cols:
                return False
            if y >= self.rows:
                return False
            if y >= 0 and self.grid[y][x] is not None:
                return False
        return True

    def lock_tetromino(self, tetromino) -> None:
        for x, y in tetromino.get_cells():
            if 0 <= x < self.cols and 0 <= y < self.rows:
                self.grid[y][x] = tetromino.color

    def clear_full_lines(self) -> int:
        cols = self.cols
        rows = self.rows
        new_grid: List[List[Optional[Tuple[int, int, int]]]] = []
        cleared = 0
        for y in range(rows - 1, -1, -1):
            if all(self.grid[y][x] is not None for x in range(cols)):
                cleared += 1
            else:
                new_grid.append(self.grid[y])
        while len(new_grid) < rows:
            new_grid.append([None for _ in range(cols)])
        new_grid.reverse()
        self.grid = new_grid
        return cleared

    def reset(self) -> None:
        self.grid = [
            [None for _ in range(self.cols)] for _ in range(self.rows)
        ]

    def add_garbage_rows(self, count: int) -> None:
        """
        Добавя 'count' реда в долната част на дъската.
        Всеки ред е 'незавършен' – с произволен брой блокчета
        (от 1 до cols-1) на произволни позиции.
        """
        count = max(0, min(count, self.rows))
        if count == 0:
            return

        # Цветове за блокчетата
        colors = [
            Colors.RED,
            Colors.GREEN,
            Colors.BLUE,
            Colors.CYAN,
            Colors.YELLOW,
            Colors.MAGENTA,
            Colors.ORANGE,
        ]

        new_rows: List[List[Optional[Tuple[int, int, int]]]] = []

        for _ in range(count):
            # колко клетки да са запълнени в този ред (1 до cols-1, за да не е пълен)
            filled_cells = random.randint(1, self.cols - 1)

            # на кои позиции да са блокчетата
            filled_positions = set(random.sample(range(self.cols), filled_cells))

            row: List[Optional[Tuple[int, int, int]]] = []
            for x in range(self.cols):
                if x in filled_positions:
                    row.append(random.choice(colors))
                else:
                    row.append(None)
            new_rows.append(row)

        # Повдигаме съществуващите редове нагоре и добавяме новите отдолу
        if count >= self.rows:
            self.grid = new_rows[-self.rows:]
        else:
            self.grid = self.grid[count:] + new_rows
