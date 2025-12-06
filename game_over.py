import pygame


class GameOverScreen:
    def __init__(self, screen, colors, font, big_font):
        self.screen = screen
        self.colors = colors
        self.font = font
        self.big_font = big_font

        self.restart_button = None
        self.quit_button = None

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "restart"
                if event.key == pygame.K_ESCAPE:
                    return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if self.restart_button and self.restart_button.collidepoint(mx, my):
                    return "restart"

                if self.quit_button and self.quit_button.collidepoint(mx, my):
                    return "quit"

        return None

    def draw(self):
        width = self.screen.get_width()
        height = self.screen.get_height()

        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        white = self.colors["WHITE"]

        title_txt = self.big_font.render("GAME OVER", True, white)
        title_rect = title_txt.get_rect(center=(width // 2, height // 2 - 90))
        self.screen.blit(title_txt, title_rect)

        sub_txt = self.font.render("Enter = НОВА ИГРА, Esc = ИЗХОД", True, white)
        sub_rect = sub_txt.get_rect(center=(width // 2, height // 2 - 50))
        self.screen.blit(sub_txt, sub_rect)

        self.restart_button = pygame.Rect(width // 2 - 170, height // 2, 150, 55)
        self.quit_button = pygame.Rect(width // 2 + 20, height // 2, 150, 55)

        pygame.draw.rect(self.screen, (0, 180, 0), self.restart_button)
        pygame.draw.rect(self.screen, (180, 0, 0), self.quit_button)

        restart_txt = self.font.render("НОВА ИГРА", True, white)
        quit_txt = self.font.render("ИЗХОД", True, white)

        self.screen.blit(restart_txt, restart_txt.get_rect(center=self.restart_button.center))
        self.screen.blit(quit_txt, quit_txt.get_rect(center=self.quit_button.center))

        pygame.display.flip()
