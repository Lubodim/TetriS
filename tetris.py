import sys
import pygame

pygame.init()

WIDHT = 500
HEIGHT = 600

screen = pygame.display.set_mode((WIDHT, HEIGHT))
pygame.display.set_caption("My Lovely TetriS")

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30,30,30))