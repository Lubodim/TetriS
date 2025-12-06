import pygame
from config import Config, Colors
from shape_factory import Tetromino


class Sidebar:
    def __init__(self, config: Config, font: pygame.font.Font, big_font: pygame.font.Font):
        self.config = config
        self.font = font
        self.big_font = big_font
        self.colors = Colors
        self.board_px_width = config.cols * config.tile_size
        self.width = config.sidebar_width
        self.height = config.rows * config.tile_size

    def draw(self, screen: pygame.Surface, score: int, lines: int, level: int, next_piece: Tetromino | None) -> None:
        x0 = self.board_px_width
        y0 = 0
        sidebar_rect = pygame.Rect(x0, y0, self.width, self.height)
        pygame.draw.rect(screen, self.colors.GRAY, sidebar_rect)
        margin = 20
        y = margin
        white = self.colors.WHITE
        title_surf = self.big_font.render("TETRIS", True, white)
        screen.blit(title_surf, (x0 + margin, y))
        y += title_surf.get_height() + 25

        def draw_label_value(label: str, value: int):
            nonlocal y
            label_surf = self.font.render(f"{label}:", True, white)
            value_surf = self.font.render(str(value), True, white)
            screen.blit(label_surf, (x0 + margin, y))
            screen.blit(value_surf, (x0 + margin, y + label_surf.get_height()))
            y += label_surf.get_height() + value_surf.get_height() + 10

        draw_label_value("Score", score)
        draw_label_value("Lines", lines)
        draw_label_value("Level", level)
        y += 10
        next_label = self.font.render("Next:", True, white)
        screen.blit(next_label, (x0 + margin, y))
        y += next_label.get_height() + 10
        preview_height = self.config.tile_size * 5
        preview_rect = pygame.Rect(
            x0 + margin,
            y,
            self.width - 2 * margin,
            preview_height,
        )
        pygame.draw.rect(screen, self.colors.DARK_GRAY, preview_rect, border_radius=8)
        pygame.draw.rect(screen, self.colors.BLACK, preview_rect, 2, border_radius=8)
        if next_piece is not None:
            self._draw_next_piece(screen, preview_rect, next_piece)

    def _draw_next_piece(self, screen: pygame.Surface, rect: pygame.Rect, next_piece: Tetromino) -> None:
        tile = self.config.tile_size // 2
        blocks = next_piece.blocks
        if not blocks:
            return
        xs = [bx for bx, _ in blocks]
        ys = [by for _, by in blocks]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        width_cells = max_x - min_x + 1
        height_cells = max_y - min_y + 1
        shape_px_width = width_cells * tile
        shape_px_height = height_cells * tile
        start_x = rect.x + (rect.width - shape_px_width) // 2
        start_y = rect.y + (rect.height - shape_px_height) // 2
        for bx, by in blocks:
            px = start_x + (bx - min_x) * tile
            py = start_y + (by - min_y) * tile
            cell_rect = pygame.Rect(px, py, tile, tile)
            pygame.draw.rect(screen, next_piece.color, cell_rect)
            pygame.draw.rect(screen, self.colors.BLACK, cell_rect, 1)
