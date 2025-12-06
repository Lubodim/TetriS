import sys
import pygame

from config import Config
from shape_factory import TetroFactory, Tetromino


def draw_grid(screen, config: Config):
    cols = config.cols
    rows = config.rows
    tile = config.tile_size
    colors = config.colors

    for y in range(rows):
        for x in range(cols):
            rect = pygame.Rect(x * tile, y * tile, tile, tile)

            pygame.draw.rect(screen, colors["GRAY"], rect)
            pygame.draw.rect(screen, colors["BLACK"], rect, 1)


def draw_tetromino(screen, config: Config, tetromino: Tetromino):
    tile = config.tile_size
    colors = config.colors

    for (x, y) in tetromino.get_cells():
        if y < 0:
            continue

        rect = pygame.Rect(x * tile, y * tile, tile, tile)
        pygame.draw.rect(screen, tetromino.color, rect)
        pygame.draw.rect(screen, colors["BLACK"], rect, 1)


def is_valid_position(tetromino: Tetromino, config: Config) -> bool:
    return tetromino.is_within_bounds(config.cols, config.rows)


def main():
    pygame.init()

    config = Config()
    colors = config.colors

    width = config.cols * config.tile_size + config.sidebar_width
    height = config.rows * config.tile_size

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("My Lovely TetriS")
    clock = pygame.time.Clock()

    running = True

    current_piece = TetroFactory.create_random(config.cols)

    fall_interval_ms = 500
    last_fall_time = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.move(-1, 0)
                    if not is_valid_position(current_piece, config):
                        current_piece.move(1, 0)

                elif event.key == pygame.K_RIGHT:
                    current_piece.move(1, 0)
                    if not is_valid_position(current_piece, config):
                        current_piece.move(-1, 0)

                elif event.key == pygame.K_DOWN:
                    current_piece.move(0, 1)
                    if not is_valid_position(current_piece, config):
                        current_piece.move(0, -1)

                elif event.key == pygame.K_UP:
                    old_blocks = current_piece.blocks.copy()
                    current_piece.rotate()
                    if not is_valid_position(current_piece, config):
                        current_piece.blocks = old_blocks

        now = pygame.time.get_ticks()
        if now - last_fall_time >= fall_interval_ms:
            test_piece = Tetromino(
                current_piece.x,
                current_piece.y,
                list(current_piece.blocks),
                current_piece.color,
            )
            test_piece.move(0, 1)

            if is_valid_position(test_piece, config):
                current_piece.move(0, 1)
            else:
                current_piece = TetroFactory.create_random(config.cols)

            last_fall_time = now

        screen.fill(colors["DARK_GRAY"])
        draw_grid(screen, config)
        draw_tetromino(screen, config, current_piece)

        pygame.display.flip()
        clock.tick(config.fps)

    pygame.quit()
    sys.exit()


main()
