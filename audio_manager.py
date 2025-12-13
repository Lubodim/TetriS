# audio_manager.py
from __future__ import annotations

from typing import Dict, Optional

import pygame


class SoundManager:
    """
    Отговаря за:
    - музика (фонови мелодии)
    - звукови ефекти (SFX) – move, rotate, drop, clear и т.н.

    Работи заедно с GameSettings:
      settings.music_on  -> включва / изключва музика
      settings.sfx_on    -> включва / изключва ефекти
    """

    def __init__(self, settings):
        self.settings = settings

        # Инициализация на mixer (safe за многократно извикване)
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # Пътища до музикалните файлове – СЕГА в assets/audio
        self.music_files: Dict[str, str] = {
            # направи така, че тези пътища да отговарят на твоята структура
            "start": "assets/audio/START.wav",        # меню + ниски нива
            "fast": "assets/audio/FAST.wav",          # средни нива
            "high": "assets/audio/HIGH SPEED.wav",    # високи нива
            "pause": "assets/audio/PAUSE.wav",        # пауза (ESC)
            "game_over": "assets/audio/GAME OVER.wav" # край на играта
        }

        # Пътища до SFX – в assets/asx (както каза)
        self.sfx_files: Dict[str, str] = {
            "button": "assets/asx/BUTTON CLICK.ogg",
            "rotate": "assets/asx/ROTATE.ogg",
            "hard_drop": "assets/asx/FAST DOWN.ogg",
            "row_clear": "assets/asx/ROW CLEAR.ogg",
            "row_clear_4": "assets/asx/FOUR ROWS CLEAR.ogg",
        }

        self.sfx_cache: Dict[str, pygame.mixer.Sound] = {}
        self.current_music_key: Optional[str] = None

    # ---------- Вътрешни помощници ----------

    def _play_music_file(self, key: str, loop: bool = True) -> None:
        """Пуска конкретен музикален файл по ключ от self.music_files."""
        if not self.settings.music_on:
            # Ако музиката е изключена, спираме всичко
            if self.current_music_key is not None:
                pygame.mixer.music.stop()
                self.current_music_key = None
            return

        filename = self.music_files.get(key)
        if not filename:
            return

        # Ако вече свири същата мелодия – нищо не правим
        if self.current_music_key == key:
            return

        try:
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play(-1 if loop else 0)
            self.current_music_key = key
        except pygame.error:
            # Ако файлът липсва или е проблемен – просто мълчим
            self.current_music_key = None

    def _stop_music(self) -> None:
        pygame.mixer.music.stop()
        self.current_music_key = None

    def _get_sfx(self, key: str) -> Optional[pygame.mixer.Sound]:
        """Лениво зареждане на SFX, кеширане в паметта."""
        if key in self.sfx_cache:
            return self.sfx_cache[key]

        filename = self.sfx_files.get(key)
        if not filename:
            return None

        try:
            sound = pygame.mixer.Sound(filename)
        except pygame.error:
            return None

        self.sfx_cache[key] = sound
        return sound

    # ---------- Публичен API ----------

    def update_music(self, state: str, level: int, game_over: bool, paused: bool) -> None:
        """
        Вика се всеки кадър от Game.run().
        На база на:
          - state: "menu", "options", "playing"
          - level: текущото ниво
          - game_over: True / False
          - paused: True / False (нашата пауза с ESC)
        избира подходящата музика.
        """

        # Ако музиката е изключена от Options – спираме и излизаме
        if not self.settings.music_on:
            if self.current_music_key is not None:
                self._stop_music()
            return

        # --- MENU / OPTIONS ---
        if state in ("menu", "options"):
            self._play_music_file("start", loop=True)
            return

        # --- PLAYING ---
        if state == "playing":
            if game_over:
                if paused:
                    # Пауза (ESC)
                    self._play_music_file("pause", loop=True)
                else:
                    # Истински Game Over
                    self._play_music_file("game_over", loop=False)
                return

            # Нормална игра – фон според нивото
            if level <= 3:
                self._play_music_file("start", loop=True)
            elif 4 <= level <= 7:
                self._play_music_file("fast", loop=True)
            else:
                self._play_music_file("high", loop=True)

    def play_sfx(self, key: str) -> None:
        """
        Пуска кратък звуков ефект (ако е включен SFX).
        Примери за ключове:
          - "button"
          - "rotate"
          - "hard_drop"
          - "row_clear"
          - "row_clear_4"
        """
        if not self.settings.sfx_on:
            return

        sound = self._get_sfx(key)
        if sound is None:
            return

        try:
            sound.play()
        except pygame.error:
            pass

    def stop_all(self) -> None:
        """Спира всичко (музика + ефекти)."""
        self._stop_music()
        pygame.mixer.stop()
