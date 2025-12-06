import sys
import pygame
from config import Config


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


def main():
    pygame.init()

    config = Config()
    running = True

    colors = config.colors

    width = config.cols * config.tile_size + config.sidebar_width
    height = config.rows * config.tile_size

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("My Lovely TetriS")
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(colors["DARK_GRAY"])
        draw_grid(screen, config)

        pygame.display.flip()
        clock.tick(config.fps)

    pygame.quit()
    sys.exit()


main()
