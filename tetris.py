import sys
import pygame

pygame.init()

WIDHT = 500
HEIGHT = 600

WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
LIGHT_GRAY = (90, 90, 90)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (50, 205, 50)
BLUE = (65, 105, 225)
CYAN = (0, 206, 209)
YELLOW = (255, 215, 0)
MAGENTA = (186, 85, 211)
ORANGE = (255, 140, 0)
DARK_GRAY = (30,30,30)




screen = pygame.display.set_mode((WIDHT, HEIGHT))
pygame.display.set_caption("My Lovely TetriS")

clock = pygame.time.Clock()

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(DARK_GRAY)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()

main()