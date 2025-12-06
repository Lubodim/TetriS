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
                elif event.key == pygame.K_RIGHT:
                    current_piece.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    if current_piece.can_move_down(config.rows):
                        current_piece.move(0, 1)
                elif event.key == pygame.K_UP:
                    current_piece.rotate()

        now = pygame.time.get_ticks()
        if now - last_fall_time >= fall_interval_ms:
            if current_piece.can_move_down(config.rows):
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
