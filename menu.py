import pygame
from config import Colors


class GameSettings:
    def __init__(self):
        self.music_on = True
        self.sfx_on = True
        self.start_level = 1


class MainMenu:
    def __init__(self, screen, font, big_font):
        self.screen = screen
        self.font = font
        self.big_font = big_font
        self.colors = Colors

        self.play_button = None
        self.options_button = None
        self.quit_button = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if self.play_button.collidepoint(mx, my):
                    return "play"
                if self.options_button.collidepoint(mx, my):
                    return "options"
                if self.quit_button.collidepoint(mx, my):
                    return "quit"
        return None

    def draw(self):
        w, h = self.screen.get_size()
        self.screen.fill(Colors.DARK_GRAY)

        title = self.big_font.render("TETRIS", True, Colors.WHITE)
        self.screen.blit(title, title.get_rect(center=(w // 2, 120)))

        button_w, button_h = 250, 60
        start_y = 250

        self.play_button = pygame.Rect(w // 2 - button_w // 2, start_y, button_w, button_h)
        self.options_button = pygame.Rect(w // 2 - button_w // 2, start_y + 80, button_w, button_h)
        self.quit_button = pygame.Rect(w // 2 - button_w // 2, start_y + 160, button_w, button_h)

        pygame.draw.rect(self.screen, Colors.GREEN, self.play_button)
        pygame.draw.rect(self.screen, Colors.BLUE, self.options_button)
        pygame.draw.rect(self.screen, Colors.RED, self.quit_button)

        play_txt = self.font.render("PLAY", True, Colors.WHITE)
        options_txt = self.font.render("OPTIONS", True, Colors.WHITE)
        quit_txt = self.font.render("QUIT", True, Colors.WHITE)

        self.screen.blit(play_txt, play_txt.get_rect(center=self.play_button.center))
        self.screen.blit(options_txt, options_txt.get_rect(center=self.options_button.center))
        self.screen.blit(quit_txt, quit_txt.get_rect(center=self.quit_button.center))


class OptionsMenu:
    def __init__(self, screen, font, big_font, settings: GameSettings):
        self.screen = screen
        self.font = font
        self.big_font = big_font
        self.settings = settings
        self.colors = Colors

        self.music_button = None
        self.sfx_button = None
        self.slider_rect = None
        self.back_button = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                if self.music_button.collidepoint(mx, my):
                    self.settings.music_on = not self.settings.music_on

                if self.sfx_button.collidepoint(mx, my):
                    self.settings.sfx_on = not self.settings.sfx_on

                if self.back_button.collidepoint(mx, my):
                    return "back"

                if self.slider_rect.collidepoint(mx, my):
                    relative = mx - self.slider_rect.x
                    new_level = int((relative / self.slider_rect.width) * 9) + 1
                    self.settings.start_level = max(1, min(10, new_level))

        return None

    def draw(self):
        w, h = self.screen.get_size()
        self.screen.fill(Colors.DARK_GRAY)

        title = self.big_font.render("OPTIONS", True, Colors.WHITE)
        self.screen.blit(title, title.get_rect(center=(w // 2, 100)))

        # Music toggle
        music_label = self.font.render(f"Music: {'On' if self.settings.music_on else 'Off'}", True, Colors.WHITE)
        self.music_button = pygame.Rect(w // 2 - 150, 200, 300, 50)
        pygame.draw.rect(self.screen, Colors.BLUE, self.music_button)
        self.screen.blit(music_label, music_label.get_rect(center=self.music_button.center))

        # SFX toggle
        sfx_label = self.font.render(f"SFX: {'On' if self.settings.sfx_on else 'Off'}", True, Colors.WHITE)
        self.sfx_button = pygame.Rect(w // 2 - 150, 280, 300, 50)
        pygame.draw.rect(self.screen, Colors.BLUE, self.sfx_button)
        self.screen.blit(sfx_label, sfx_label.get_rect(center=self.sfx_button.center))

        # Start Level Slider
        slider_label = self.font.render("START LEVEL", True, Colors.WHITE)
        self.screen.blit(slider_label, (w // 2 - 60, 360))

        self.slider_rect = pygame.Rect(w // 2 - 150, 400, 300, 10)
        pygame.draw.rect(self.screen, Colors.WHITE, self.slider_rect)

        knob_x = self.slider_rect.x + (self.settings.start_level - 1) * (self.slider_rect.width // 9)
        knob_rect = pygame.Rect(knob_x - 8, self.slider_rect.y - 10, 16, 30)
        pygame.draw.rect(self.screen, Colors.YELLOW, knob_rect)

        level_txt = self.font.render(str(self.settings.start_level), True, Colors.WHITE)
        self.screen.blit(level_txt, level_txt.get_rect(center=(w // 2, 450)))

        # Back button
        self.back_button = pygame.Rect(w // 2 - 100, 520, 200, 50)
        pygame.draw.rect(self.screen, Colors.RED, self.back_button)
        back_txt = self.font.render("BACK", True, Colors.WHITE)
        self.screen.blit(back_txt, back_txt.get_rect(center=self.back_button.center))
