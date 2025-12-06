import sys
import pygame

from config import Config
from shape_factory import TetroFactory, Tetromino
from board import Board


class Game:
    def __init__(self, config: Config):
        pygame.init()

        self.config = config
        self.colors = config.colors

        width = config.cols * config.tile_size + config.sidebar_width
        height = config.rows * config.tile_size

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("My Lovely TetriS")
        self.clock = pygame.time.Clock()

        self.board = Board(config)
        self.current_piece = TetroFactory.create_random(config.cols)

        self.fall_interval_ms = 500
        self.last_fall_time = pygame.time.get_ticks()
        self.running = True

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.config.fps)

        pygame.quit()
        sys.exit()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:

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
                    self.board.lock_tetromino(self.current_piece)
                    self.board.clear_full_lines()
                    self.spawn_new_piece()


    def move_current_piece(self, dx: int, dy: int):
        self.current_piece.move(dx, dy)
        if not self.board.is_valid_position(self.current_piece):
            # връщаме обратно
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
        self.current_piece = TetroFactory.create_random(self.config.cols)

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
                self.board.lock_tetromino(self.current_piece)
                self.board.clear_full_lines()
                self.spawn_new_piece()

            self.last_fall_time = now


    def draw_tetromino(self, tetromino: Tetromino):
        tile = self.config.tile_size
        colors = self.colors

        for (x, y) in tetromino.get_cells():
            if y < 0:
                continue

            rect = pygame.Rect(x * tile, y * tile, tile, tile)
            pygame.draw.rect(self.screen, tetromino.color, rect)
            pygame.draw.rect(self.screen, colors["BLACK"], rect, 1)

    def draw(self):
        self.screen.fill(self.colors["DARK_GRAY"])
        self.board.draw(self.screen)
        self.draw_tetromino(self.current_piece)
        pygame.display.flip()
