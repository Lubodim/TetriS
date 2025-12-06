import sys
import pygame


WIDHT = 500
HEIGHT = 600

WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
LIGHT_GRAY = (90, 90, 90)
DARK_GRAY = (30,30,30)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (50, 205, 50)
BLUE = (65, 105, 225)
CYAN = (0, 206, 209)
YELLOW = (255, 215, 0)
MAGENTA = (186, 85, 211)
ORANGE = (255, 140, 0)



def get_config():
    return {
        "cols": 10,
        "rows": 20,
        "tile_size": 30,
        "sidebar_width": 200,
        "fps": 60,
        "colors": {
            "WHITE": WHITE,
            "GRAY": GRAY,
            "DARK_GRAY": DARK_GRAY,
            "BLACK": BLACK

        }
    }

def draw_grid(screen, config):
    cols = config["cols"]
    rows = config["rows"]
    tile = config["tile_size"]
    colors = config["colors"]

    for y in range(rows):
        for x in range(cols):
            rect = pygame.Rect(x * tile, y * tile, tile, tile)

            pygame.draw.rect(screen, colors["GRAY"], rect)
            pygame.draw.rect(screen, colors["BLACK"], rect, 1)


def main():
    pygame.init()

    running = True

    config = get_config()
    colors = config["colors"]

    width = config["cols"] * config["tile_size"] + config["sidebar_width"]
    height = config["rows"] * config["tile_size"]

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
        clock.tick(config["fps"])
    pygame.quit()
    sys.exit()

main()