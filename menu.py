import pygame
from config import Colors
from audio_manager import SoundManager


class GameSettings:
    def __init__(self):
        self.music_on = True
        self.sfx_on = True
        self._start_level = 0
        self._difficulty = 0

    @property
    def start_level(self) -> int:
        return self._start_level

    @start_level.setter
    def start_level(self, value: int) -> None:
        # позволяваме 0–10
        v = int(value)
        self._start_level = max(0, min(10, v))

    @property
    def difficulty(self) -> int:
        return self._difficulty

    @difficulty.setter
    def difficulty(self, value: int) -> None:
        # позволяваме 0–16
        v = int(value)
        self._difficulty = max(0, min(16, v))


class MainMenu:
    def __init__(self, screen, font, big_font, sounds: SoundManager | None = None):
        self.screen = screen
        self.font = font
        self.big_font = big_font
        self.colors = Colors
        self.sounds = sounds

        self.play_button = None
        self.options_button = None
        self.quit_button = None

    def _click_sfx(self):
        if self.sounds:
            self.sounds.play_sfx("button")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if self.play_button and self.play_button.collidepoint(mx, my):
                    self._click_sfx()
                    return "play"
                if self.options_button and self.options_button.collidepoint(mx, my):
                    self._click_sfx()
                    return "options"
                if self.quit_button and self.quit_button.collidepoint(mx, my):
                    self._click_sfx()
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
    def __init__(self, screen, font, big_font, settings: GameSettings, sounds: SoundManager | None = None):
        self.screen = screen
        self.font = font
        self.big_font = big_font
        self.settings = settings
        self.colors = Colors
        self.sounds = sounds

        self.music_button = None
        self.sfx_button = None
        self.slider_rect = None          # за START LEVEL
        self.difficulty_slider_rect = None  # за DIFFICULTY
        self.back_button = None

    def _click_sfx(self):
        if self.sounds:
            self.sounds.play_sfx("button")

    def _value_from_slider(self, mouse_x: int, rect: pygame.Rect, min_value: int, max_value: int) -> int:
        # Нормализиране на позицията в [0, width]
        relative = max(0, min(rect.width, mouse_x - rect.x))
        steps = max_value - min_value
        if steps <= 0:
            return min_value
        ratio = relative / rect.width
        value = int(round(ratio * steps)) + min_value
        return max(min_value, min(max_value, value))

    def _knob_x_from_value(self, rect: pygame.Rect, value: int, min_value: int, max_value: int) -> int:
        steps = max_value - min_value
        if steps <= 0:
            return rect.x
        ratio = (value - min_value) / steps
        return rect.x + int(ratio * rect.width)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                if self.music_button and self.music_button.collidepoint(mx, my):
                    self.settings.music_on = not self.settings.music_on
                    self._click_sfx()

                if self.sfx_button and self.sfx_button.collidepoint(mx, my):
                    self.settings.sfx_on = not self.settings.sfx_on
                    self._click_sfx()

                if self.back_button and self.back_button.collidepoint(mx, my):
                    self._click_sfx()
                    return "back"

                # Плъзгач за START LEVEL (0–10)
                if self.slider_rect and self.slider_rect.collidepoint(mx, my):
                    new_level = self._value_from_slider(mx, self.slider_rect, 0, 10)
                    self.settings.start_level = new_level
                    self._click_sfx()

                # Плъзгач за DIFFICULTY (0–16)
                if self.difficulty_slider_rect and self.difficulty_slider_rect.collidepoint(mx, my):
                    new_diff = self._value_from_slider(mx, self.difficulty_slider_rect, 0, 16)
                    self.settings.difficulty = new_diff
                    self._click_sfx()

        return None

    def draw(self):
        w, h = self.screen.get_size()
        self.screen.fill(Colors.DARK_GRAY)

        # === Лейаут параметри ===
        top_margin = 70
        spacing = 70
        slider_block_space = 55  # вътрешно разстояние в блока (label -> slider -> value)

        # === Заглавие ===
        title = self.big_font.render("OPTIONS", True, Colors.WHITE)
        self.screen.blit(title, title.get_rect(center=(w // 2, top_margin)))

        # === MUSIC ===
        music_y = top_margin + spacing
        self.music_button = pygame.Rect(w // 2 - 150, music_y, 300, 50)
        pygame.draw.rect(self.screen, Colors.BLUE, self.music_button)
        music_label = self.font.render(
            f"Music: {'On' if self.settings.music_on else 'Off'}",
            True,
            Colors.WHITE,
        )
        self.screen.blit(music_label, music_label.get_rect(center=self.music_button.center))

        # === SFX ===
        sfx_y = music_y + spacing
        self.sfx_button = pygame.Rect(w // 2 - 150, sfx_y, 300, 50)
        pygame.draw.rect(self.screen, Colors.BLUE, self.sfx_button)
        sfx_label = self.font.render(
            f"SFX: {'On' if self.settings.sfx_on else 'Off'}",
            True,
            Colors.WHITE,
        )
        self.screen.blit(sfx_label, sfx_label.get_rect(center=self.sfx_button.center))

        # === START LEVEL ===
        start_label_y = sfx_y + spacing + 15
        start_slider_y = start_label_y + 15
        start_value_y = start_slider_y + slider_block_space

        start_label = self.font.render("START LEVEL", True, Colors.WHITE)
        self.screen.blit(start_label, start_label.get_rect(center=(w // 2, start_label_y)))

        self.slider_rect = pygame.Rect(w // 2 - 150, start_slider_y, 300, 10)
        pygame.draw.rect(self.screen, Colors.WHITE, self.slider_rect)

        knob_x = self._knob_x_from_value(self.slider_rect, self.settings.start_level, 0, 10)
        knob_rect = pygame.Rect(knob_x - 8, self.slider_rect.y - 10, 16, 30)
        pygame.draw.rect(self.screen, Colors.YELLOW, knob_rect)

        level_txt = self.font.render(str(self.settings.start_level), True, Colors.WHITE)
        self.screen.blit(level_txt, level_txt.get_rect(center=(w // 2, start_value_y)))

        # === DIFFICULTY ===
        diff_label_y = start_value_y + spacing - 10
        diff_slider_y = diff_label_y + 15
        diff_value_y = diff_slider_y + slider_block_space

        diff_label = self.font.render("DIFFICULTY", True, Colors.WHITE)
        self.screen.blit(diff_label, diff_label.get_rect(center=(w // 2, diff_label_y)))

        self.difficulty_slider_rect = pygame.Rect(w // 2 - 150, diff_slider_y, 300, 10)
        pygame.draw.rect(self.screen, Colors.WHITE, self.difficulty_slider_rect)

        diff_knob_x = self._knob_x_from_value(self.difficulty_slider_rect, self.settings.difficulty, 0, 16)
        diff_knob_rect = pygame.Rect(diff_knob_x - 8, self.difficulty_slider_rect.y - 10, 16, 30)
        pygame.draw.rect(self.screen, Colors.ORANGE, diff_knob_rect)

        diff_txt = self.font.render(str(self.settings.difficulty), True, Colors.WHITE)
        self.screen.blit(diff_txt, diff_txt.get_rect(center=(w // 2, diff_value_y)))

        # === BACK BUTTON ===
        back_y = diff_value_y + spacing - 20
        self.back_button = pygame.Rect(w // 2 - 100, back_y, 200, 50)
        pygame.draw.rect(self.screen, Colors.RED, self.back_button)
        back_txt = self.font.render("BACK", True, Colors.WHITE)
        self.screen.blit(back_txt, back_txt.get_rect(center=self.back_button.center))
