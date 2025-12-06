import sys
import pygame

from config import Config, Colors
from shape_factory import TetroFactory, Tetromino
from board import Board
from game_over import GameOverScreen
from sidebar import Sidebar


class Game:
    def __init__(self, config: Config):
        pygame.init()
        self.config = config
        self.colors = Colors
        width = config.cols * config.tile_size + config.sidebar_width
        height = config.rows * config.tile_size
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("My Lovely TetriS")
        self.clock = pygame.time.Clock()
        self.board = Board(config)
        self.current_piece = TetroFactory.create_random(config.cols)
        self.next_piece = TetroFactory.create_random(config.cols)
        self.fall_interval_ms = 500
        self.last_fall_time = pygame.time.get_ticks()
        self.running = True
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.font = pygame.font.SysFont("consolas", 20)
        self.big_font = pygame.font.SysFont("consolas", 32, bold=True)
        self.sidebar = Sidebar(config, self.font, self.big_font)
        self.game_over = False
        self.game_over_screen = GameOverScreen(
            self.screen, self.colors, self.font, self.big_font
        )

    def run(self):
        while self.running:
            if self.game_over:
                action = self.game_over_screen.handle_events()
                self.draw()
                self.game_over_screen.draw()
                pygame.display.flip()
                if action == "quit":
                    self.running = False
                elif action == "restart":
                    self.reset_game()
                elif action == "continue":
                    self.game_over = False
            else:
                self.handle_events()
                self.update()
                self.draw()
                pygame.display.flip()
            self.clock.tick(self.config.fps)
        pygame.quit()
        sys.exit()

    def reset_game(self):
        self.board = Board(self.config)
        self.current_piece = TetroFactory.create_random(self.config.cols)
        self.next_piece = TetroFactory.create_random(self.config.cols)
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.fall_interval_ms = 500
        self.game_over = False
        self.last_fall_time = pygame.time.get_ticks()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_over = True
                    return
                if event.key == pygame.K_LEFT:
                    self.move_current_piece(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.move_current_piece(1, 0)
                elif event.key == pygame.K_DOWN:
                    self.move_current_piece(0, 1)
                elif event.key == pygame.K_UP:
                    self.rotate_current_piece()
                elif event.key == pygame.K_SPACE:
                    self.hard_drop()
                    self.on_piece_landed()

    def move_current_piece(self, dx: int, dy: int):
        self.current_piece.move(dx, dy)
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.move(-dx, -dy)

    def rotate_current_piece(self):
        old_blocks = self.current_piece.blocks.copy()
        self.current_piece.rotate()
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.blocks = old_blocks

    def hard_drop(self):
        while True:
            test_piece = Tetromino(
                self.current_piece.x,
                self.current_piece.y,
                list(self.current_piece.blocks),
                self.current_piece.color,
            )
            test_piece.move(0, 1)
            if self.board.is_valid_position(test_piece):
                self.current_piece.move(0, 1)
            else:
                break

    def spawn_new_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = TetroFactory.create_random(self.config.cols)
        if not self.board.is_valid_position(self.current_piece):
            self.game_over = True

    def calculate_score(self, cleared: int) -> int:
        base = {1: 100, 2: 300, 3: 500, 4: 800}.get(cleared, cleared * 100)
        return base * self.level

    def on_piece_landed(self):
        self.board.lock_tetromino(self.current_piece)
        cleared = self.board.clear_full_lines()
        if cleared > 0:
            self.lines_cleared += cleared
            self.score += self.calculate_score(cleared)
            self.level = min(10, 1 + self.lines_cleared // 100)
            self.fall_interval_ms = max(120, 500 - (self.level - 1) * 30)
        self.spawn_new_piece()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_fall_time >= self.fall_interval_ms:
            test_piece = Tetromino(
                self.current_piece.x,
                self.current_piece.y,
                list(self.current_piece.blocks),
                self.current_piece.color,
            )
            test_piece.move(0, 1)
            if self.board.is_valid_position(test_piece):
                self.current_piece.move(0, 1)
            else:
                self.on_piece_landed()
            self.last_fall_time = now

    def draw_tetromino(self, tetromino: Tetromino):
        tile = self.config.tile_size
        colors = self.colors
        for x, y in tetromino.get_cells():
            if y < 0:
                continue
            rect = pygame.Rect(x * tile, y * tile, tile, tile)
            pygame.draw.rect(self.screen, tetromino.color, rect)
            pygame.draw.rect(self.screen, colors.BLACK, rect, 1)

    def draw(self):
        self.screen.fill(self.colors.DARK_GRAY)
        self.board.draw(self.screen)
        if not self.game_over:
            self.draw_tetromino(self.current_piece)
        self.sidebar.draw(
            self.screen,
            score=self.score,
            lines=self.lines_cleared,
            level=self.level,
            next_piece=self.next_piece,
        )
