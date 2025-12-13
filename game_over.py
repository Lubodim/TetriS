import pygame


class GameOverScreen:
    def __init__(self, screen, colors, font, big_font, sounds=None):
        self.screen = screen
        self.colors = colors
        self.font = font
        self.big_font = big_font
        self.sounds = sounds

        self.restart_button = None
        self.continue_button = None
        self.quit_button = None

    def _click_sfx(self):
        if self.sounds:
            self.sounds.play_sfx("button")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self._click_sfx()
                    return "restart"
                if event.key == pygame.K_SPACE:
                    self._click_sfx()
                    return "continue"
                if event.key == pygame.K_ESCAPE:
                    self._click_sfx()
                    return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if self.restart_button and self.restart_button.collidepoint(mx, my):
                    self._click_sfx()
                    return "restart"
                if self.continue_button and self.continue_button.collidepoint(mx, my):
                    self._click_sfx()
                    return "continue"
                if self.quit_button and self.quit_button.collidepoint(mx, my):
                    self._click_sfx()
                    return "quit"
        return None

    def draw(self):
        width, height = self.screen.get_size()
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        white = self.colors.WHITE
        title_txt = self.big_font.render("GAME OVER", True, white)
        title_rect = title_txt.get_rect(center=(width // 2, height // 2 - 160))
        self.screen.blit(title_txt, title_rect)
        button_width = 200
        button_height = 55
        spacing = 20
        center_x = width // 2
        start_y = height // 2 - (button_height * 3 + spacing * 2) // 2
        self.restart_button = pygame.Rect(center_x - button_width // 2, start_y, button_width, button_height)
        self.continue_button = pygame.Rect(center_x - button_width // 2, start_y + button_height + spacing, button_width, button_height)
        self.quit_button = pygame.Rect(center_x - button_width // 2, start_y + (button_height + spacing) * 2, button_width, button_height)
        pygame.draw.rect(self.screen, self.colors.GREEN, self.restart_button)
        pygame.draw.rect(self.screen, self.colors.BLUE, self.continue_button)
        pygame.draw.rect(self.screen, self.colors.RED, self.quit_button)
        restart_txt = self.font.render("НОВА ИГРА", True, white)
        continue_txt = self.font.render("ПРОДЪЛЖИ", True, white)
        quit_txt = self.font.render("ИЗХОД", True, white)
        self.screen.blit(restart_txt, restart_txt.get_rect(center=self.restart_button.center))
        self.screen.blit(continue_txt, continue_txt.get_rect(center=self.continue_button.center))
        self.screen.blit(quit_txt, quit_txt.get_rect(center=self.quit_button.center))
