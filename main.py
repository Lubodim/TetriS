import sys
import pygame

from config import (
    Config,
    Tetromino,
    WHITE,
    LIGHT_GRAY,
    BLACK,
)
from board import Board
from shape_factory import TetrominoFactory


class Game:

    def __init__(self, config: Config):
        pygame.init()
        pygame.display.set_caption("TETRIS NPG po KTS")

        self.config = config

        width = config.cols * config.tile_size + config.sidebar_width
        height = config.rows * config.tile_size

        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        self.board = Board(config)
        self.current_piece: Tetromino = TetrominoFactory.create_random(config.cols)
        self.next_piece: Tetromino = TetrominoFactory.create_random(config.cols)

        self.score: int = 0
        self.lines_cleared: int = 0
        self.level: int = 1

        self.fall_interval_ms: int = config.initial_fall_interval_ms
        self.last_fall_time: int = pygame.time.get_ticks()

        self.font = pygame.font.SysFont("consolas", 20)
        self.big_font = pygame.font.SysFont("consolas", 32, bold=True)

        # NEW → Pause state
        self.paused = False

    # ==========================
    # MAIN LOOP
    # ==========================
    def run(self) -> None:
        while True:
            if self.paused:
                self.handle_pause_menu_events()
                self.draw_pause_menu()
            else:
                self.handle_events()
                if not self.board.game_over:
                    self.update()
                self.draw()

            self.clock.tick(self.config.fps)

    # ==========================
    # NORMAL GAME EVENTS
    # ==========================
    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # ESC → PAUSE MENU
                if event.key == pygame.K_ESCAPE:
                    self.paused = True
                    return

                if not self.board.game_over:
                    if event.key == pygame.K_LEFT:
                        self.move_current_piece(dx=-1)
                    elif event.key == pygame.K_RIGHT:
                        self.move_current_piece(dx=1)
                    elif event.key == pygame.K_DOWN:
                        self.soft_drop()
                    elif event.key == pygame.K_UP:
                        self.rotate_current_piece()
                    elif event.key == pygame.K_SPACE:
                        self.hard_drop()

    # ==========================
    # PAUSE MENU EVENTS
    # ==========================
    def handle_pause_menu_events(self):
        """Обработва събития в менюто 'ДА/НЕ' при пауза."""
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = False  # ESC → връщане към играта

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # YES button
                if self.yes_button.collidepoint(mx, my):
                    pygame.quit()
                    sys.exit()

                # NO button
                if self.no_button.collidepoint(mx, my):
                    self.paused = False

    # ==========================
    # GAME LOGIC
    # ==========================
    def update(self) -> None:
        now = pygame.time.get_ticks()
        if now - self.last_fall_time >= self.fall_interval_ms:
            self.last_fall_time = now
            if not self.move_current_piece(dy=1):
                self.board.lock_tetromino(self.current_piece)
                cleared = self.board.clear_full_lines()
                if cleared > 0:
                    self.handle_lines_cleared(cleared)

                if self.board.game_over:
                    return

                self.spawn_next_piece()

    # Movement
    def move_current_piece(self, dx: int = 0, dy: int = 0) -> bool:
        if self.board.is_valid_position(self.current_piece, dx=dx, dy=dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        return False

    def rotate_current_piece(self) -> None:
        if self.board.is_valid_position(self.current_piece, rotated=True):
            self.current_piece = self.current_piece.rotated()

    def soft_drop(self) -> None:
        self.move_current_piece(dy=1)

    def hard_drop(self) -> None:
        while self.move_current_piece(dy=1):
            pass
        self.board.lock_tetromino(self.current_piece)
        cleared = self.board.clear_full_lines()
        if cleared > 0:
            self.handle_lines_cleared(cleared)
        if not self.board.game_over:
            self.spawn_next_piece()

    # NEW — Pause menu drawing
    def draw_pause_menu(self):
        self.screen.fill((0, 0, 0))

        txt = self.big_font.render("ИСКАШ ЛИ ДА ИЗЛЕЗЕШ?", True, WHITE)
        rect = txt.get_rect(center=(self.screen.get_width() // 2, 200))
        self.screen.blit(txt, rect)

        # Buttons
        self.yes_button = pygame.Rect(self.screen.get_width() // 2 - 150, 300, 120, 50)
        self.no_button = pygame.Rect(self.screen.get_width() // 2 + 30, 300, 120, 50)

        pygame.draw.rect(self.screen, (180, 0, 0), self.yes_button)
        pygame.draw.rect(self.screen, (0, 180, 0), self.no_button)

        yes_txt = self.font.render("ДА", True, WHITE)
        no_txt = self.font.render("НЕ", True, WHITE)

        self.screen.blit(yes_txt, yes_txt.get_rect(center=self.yes_button.center))
        self.screen.blit(no_txt, no_txt.get_rect(center=self.no_button.center))

        pygame.display.flip()

    # ==========================
    # REMAINING FUNCTIONS (unchanged)
    # ==========================
    def spawn_next_piece(self) -> None:
        self.current_piece = self.next_piece
        self.next_piece = TetrominoFactory.create_random(self.config.cols)

        if not self.board.is_valid_position(self.current_piece):
            self.board.game_over = True

    def handle_lines_cleared(self, cleared: int) -> None:
        self.lines_cleared += cleared

        if cleared == 1:
            base = 40
        elif cleared == 2:
            base = 100
        elif cleared == 3:
            base = 300
        elif cleared == 4:
            base = 1200
        else:
            base = 0

        self.score += base * self.level

        new_level = 1 + self.lines_cleared // 10
        if new_level > self.level:
            self.level = new_level
            self.fall_interval_ms = max(
                self.config.min_fall_interval_ms,
                self.fall_interval_ms - self.config.fall_speed_step_ms,
            )

    # Drawing (normal)
    def draw(self) -> None:
        self.screen.fill(LIGHT_GRAY)
        self.board.draw(self.screen)
        self.draw_tetromino(self.current_piece)
        self.draw_sidebar()
        pygame.display.flip()

    def draw_tetromino(self, tetromino: Tetromino, offset_x: int = 0, offset_y: int = 0) -> None:
        tile = self.config.tile_size
        for bx, by in tetromino.blocks:
            x = tetromino.x + bx
            y = tetromino.y + by
            if y < 0:
                continue

            rect = pygame.Rect(
                offset_x + x * tile,
                offset_y + y * tile,
                tile,
                tile,
            )
            inner_rect = rect.inflate(-4, -4)
            pygame.draw.rect(self.screen, tetromino.color, inner_rect)
            pygame.draw.rect(self.screen, BLACK, rect, 1)

    def draw_sidebar(self) -> None:
        tile = self.config.tile_size
        board_width_px = self.config.cols * tile

        sidebar_rect = pygame.Rect(
            board_width_px, 0, self.config.sidebar_width, self.config.rows * tile
        )
        pygame.draw.rect(self.screen, (25, 25, 25), sidebar_rect)

        padding = 16
        x_base = board_width_px + padding
        y = padding

        title_surf = self.big_font.render("TETRIS", True, WHITE)
        self.screen.blit(title_surf, (x_base, y))
        y += title_surf.get_height() + 20

        score_surf = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_surf, (x_base, y))
        y += score_surf.get_height() + 8

        level_surf = self.font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_surf, (x_base, y))
        y += level_surf.get_height() + 8

        lines_surf = self.font.render(f"Lines: {self.lines_cleared}", True, WHITE)
        self.screen.blit(lines_surf, (x_base, y))
        y += lines_surf.get_height() + 20

        next_surf = self.font.render("Next:", True, WHITE)
        self.screen.blit(next_surf, (x_base, y))
        y += next_surf.get_height() + 8

        preview_tile = tile // 2
        preview_origin_x = x_base + 40
        preview_origin_y = y + 40

        temp_piece = Tetromino(
            x=0,
            y=0,
            blocks=self.next_piece.blocks,
            color=self.next_piece.color,
        )

        for bx, by in temp_piece.blocks:
            rect = pygame.Rect(
                preview_origin_x + bx * preview_tile,
                preview_origin_y + by * preview_tile,
                preview_tile,
                preview_tile,
            )
            inner_rect = rect.inflate(-4, -4)
            pygame.draw.rect(self.screen, temp_piece.color, inner_rect)
            pygame.draw.rect(self.screen, BLACK, rect, 1)

        if self.board.game_over:
            self.draw_game_over()

    def draw_game_over(self) -> None:
        width = self.screen.get_width()
        height = self.screen.get_height()

        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        text = "GAME OVER"
        info = "Press ESC"

        text_surf = self.big_font.render(text, True, WHITE)
        info_surf = self.font.render(info, True, WHITE)

        text_rect = text_surf.get_rect(center=(width // 2, height // 2 - 20))
        info_rect = info_surf.get_rect(center=(width // 2, height // 2 + 20))

        self.screen.blit(text_surf, text_rect)
        self.screen.blit(info_surf, info_rect)


def main() -> None:
    config = Config()
    game = Game(config)
    game.run()


if __name__ == "__main__":
    main()
