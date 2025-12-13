import sys
import pygame

from config import Config, Colors
from shape_factory import TetroFactory, Tetromino
from board import Board
from game_over import GameOverScreen
from sidebar import Sidebar
from menu import MainMenu, OptionsMenu, GameSettings
from audio_manager import SoundManager



class Game:
    def __init__(self, config: Config):
        pygame.init()

        self.config = config
        self.colors = Colors

        self.font = pygame.font.SysFont("consolas", 20)
        self.big_font = pygame.font.SysFont("consolas", 32, bold=True)

        width = config.cols * config.tile_size + config.sidebar_width
        height = config.rows * config.tile_size
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("My Lovely TetriS")

        self.clock = pygame.time.Clock()

        self.settings = GameSettings()
        self.sound = SoundManager(self.settings)
        self.state = "menu"

        # подаваме sound към менюто и game over екрана
        self.menu = MainMenu(self.screen, self.font, self.big_font, self.sound)
        self.options_menu = OptionsMenu(self.screen, self.font, self.big_font, self.settings, self.sound)

        self.board = Board(config)
        self.current_piece = TetroFactory.create_random(config.cols)
        self.next_piece = TetroFactory.create_random(config.cols)

        self.last_fall_time = pygame.time.get_ticks()
        self.running = True

        self.score = 0
        self.lines_cleared = 0
        self._level = 0
        self.fall_interval_ms = 500

        self.sidebar = Sidebar(config, self.font, self.big_font)

        self.game_over = False
        self.paused = False
        self.game_over_screen = GameOverScreen(
            self.screen, self.colors, self.font, self.big_font, self.sound
        )


    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, value: int) -> None:
        value = max(0, min(10, value))
        self._level = value
        self.fall_interval_ms = max(120, 500 - (self._level - 1) * 50)

    def run(self):
        while self.running:
            if self.state == "menu":
                action = self.menu.handle_events()
                self.menu.draw()
                pygame.display.flip()

                if action == "play":
                    # Нова игра тръгва винаги от менюто
                    self.reset_game()
                    self.state = "playing"

                elif action == "options":
                    self.state = "options"

                elif action == "quit":
                    self.running = False

            elif self.state == "options":
                action = self.options_menu.handle_events()
                self.options_menu.draw()
                pygame.display.flip()

                if action == "back":
                    self.state = "menu"
                elif action == "quit":
                    self.running = False

            elif self.state == "playing":
                if self.game_over:
                    # Пауза или Game Over – показваме екрана
                    action = self.game_over_screen.handle_events()
                    self.draw()
                    self.game_over_screen.draw()
                    pygame.display.flip()

                    if action == "continue":
                        # Продължаваме текущата игра (от пауза)
                        self.game_over = False
                        self.paused = False

                    elif action == "restart":
                        # НОВА ИГРА -> връщаме в менюто,
                        # за да може да смениш ниво и трудност
                        self.game_over = False
                        self.paused = False
                        self.state = "menu"

                    elif action == "quit":
                        # Пълно излизане от играта
                        self.running = False

                else:
                    # Нормален игрови цикъл
                    self.handle_events()
                    self.update()
                    self.draw()
                    pygame.display.flip()

            # ъпдейтваме музиката според текущото състояние
            self.sound.update_music(
                state=self.state,
                level=self.level,
                game_over=self.game_over,
                paused=self.paused,
            )

            self.clock.tick(self.config.fps)

        pygame.quit()
        sys.exit()

    def reset_game(self):
        self.board = Board(self.config)
        if self.settings.difficulty > 0:
            self.board.add_garbage_rows(self.settings.difficulty)

        self.current_piece = TetroFactory.create_random(self.config.cols)
        self.next_piece = TetroFactory.create_random(self.config.cols)

        self.score = 0
        self.lines_cleared = 0
        self.level = self.settings.start_level

        self.game_over = False
        self.paused = False  # <-- важно
        self.last_fall_time = pygame.time.get_ticks()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Пауза – показваме GameOverScreen, но с флаг paused=True
                    self.game_over = True
                    self.paused = True
                    return

                if event.key == pygame.K_LEFT:
                    self.move_current_piece(-1, 0)
                    # тук може по-късно да добавиш move SFX

                elif event.key == pygame.K_RIGHT:
                    self.move_current_piece(1, 0)
                    # тук може по-късно да добавиш move SFX

                elif event.key == pygame.K_DOWN:
                    self.move_current_piece(0, 1)
                    # ако искаш и за soft drop звук – нов SFX

                elif event.key == pygame.K_UP:
                    self.rotate_current_piece()
                    self.sound.play_sfx("rotate")

                elif event.key == pygame.K_SPACE:
                    # HARD DROP
                    self.hard_drop()
                    self.on_piece_landed()
                    self.sound.play_sfx("hard_drop")

    def move_current_piece(self, dx: int, dy: int):
        self.current_piece.move(dx, dy)
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.move(-dx, -dy)

    def rotate_current_piece(self):
        old_blocks = self.current_piece.blocks.copy()
        self.current_piece.rotate()
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.blocks = old_blocks

    def hard_drop(self):
        while True:
            test_piece = Tetromino(
                self.current_piece.x,
                self.current_piece.y,
                list(self.current_piece.blocks),
                self.current_piece.color,
            )
            test_piece.move(0, 1)
            if self.board.is_valid_position(test_piece):
                self.current_piece.move(0, 1)
            else:
                break

    def spawn_new_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = TetroFactory.create_random(self.config.cols)
        if not self.board.is_valid_position(self.current_piece):
            self.game_over = True
            self.paused = False


    def calculate_score(self, cleared: int) -> int:
        base = {1: 100, 2: 300, 3: 500, 4: 800}.get(cleared, cleared * 100)
        return base * self.level

    def on_piece_landed(self):
        self.board.lock_tetromino(self.current_piece)
        cleared = self.board.clear_full_lines()
        if cleared > 0:
            # SFX за чистене на редове – различен при 4 реда
            if cleared == 4:
                self.sound.play_sfx("row_clear_4")
            else:
                self.sound.play_sfx("row_clear")

            self.lines_cleared += cleared
            self.score += self.calculate_score(cleared)

            new_level_from_lines = 1 + self.lines_cleared // 100
            self.level = max(self.level, new_level_from_lines)

        self.spawn_new_piece()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_fall_time >= self.fall_interval_ms:
            test_piece = Tetromino(
                self.current_piece.x,
                self.current_piece.y,
                list(self.current_piece.blocks),
                self.current_piece.color,
            )
            test_piece.move(0, 1)
            if self.board.is_valid_position(test_piece):
                self.current_piece.move(0, 1)
            else:
                self.on_piece_landed()
            self.last_fall_time = now

    def draw_tetromino(self, tetromino: Tetromino):
        tile = self.config.tile_size
        colors = self.colors
        for x, y in tetromino.get_cells():
            if y < 0:
                continue
            rect = pygame.Rect(x * tile, y * tile, tile, tile)
            pygame.draw.rect(self.screen, tetromino.color, rect)
            pygame.draw.rect(self.screen, colors.BLACK, rect, 1)

    def draw(self):
        self.screen.fill(self.colors.DARK_GRAY)
        self.board.draw(self.screen)
        if not self.game_over:
            self.draw_tetromino(self.current_piece)
        self.sidebar.draw(
            self.screen,
            score=self.score,
            lines=self.lines_cleared,
            level=self.level,
            next_piece=self.next_piece,
        )
