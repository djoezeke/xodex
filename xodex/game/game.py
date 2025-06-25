"""Game"""

import os
from importlib import import_module

import pygame
from pygame.event import Event

from xodex.scenes.manager import SceneManager

# from xodex.core.localization import localize

SCENES_MODULE_NAME = "scenes"
OBJECTS_MODULE_NAME = "objects"


class Game:
    """Game"""

    def __init__(self, game: str = "", **kwargs) -> None:

        # Full Python path to the game event.g. 'hello.hello'.
        self.game = game

        pygame.init()

        if not self.game == "":
            os.environ.setdefault("XODEX_SETTINGS_MODULE", f"{self.game}.settings")

        xodex_settings = os.getenv("XODEX_SETTINGS_MODULE")

        self.setting = import_module(xodex_settings)  # TODO Fix import Error in build

        self._size = self.setting.WINDOW_SIZE or (560, 480)
        self._caption = self.setting.TITLE or "Xodex"
        self._icon = self.setting.ICON_PATH or "Xodex"
        self._fps = self.setting.FPS or 60
        self._debug = self.setting.DEBUG or False
        self._fullscreen = self.setting.FULLSCREEN or False
        self._mainscene = self.setting.MAIN_SCENE or "XodexMainScene"
        self._show_fps = getattr(self.setting, "SHOW_FPS", False)
        self._font = pygame.font.SysFont("Arial", 18)
        self._debug_overlay = False

        self.__screen = pygame.display.set_mode(self._size, pygame.SCALED | pygame.RESIZABLE)

        if self._fullscreen:
            self.__screen = pygame.display.set_mode(self._size, pygame.SCALED | pygame.RESIZABLE | pygame.FULLSCREEN)

        self.__clock = pygame.time.Clock()
        self._paused = False

        # Whether the registry is populated.
        self.ready = self.objects_ready = self.scenes_ready = False

        pygame.display.set_caption(self._caption)
        scene = SceneManager().get_scene(self._mainscene)
        SceneManager().reset(scene())

    # region Exit

    def __process_exit_events(self, event: Event) -> None:
        if event.type == pygame.QUIT:
            self.exit_game()

    def exit_game(self) -> None:
        """Cleanly exit the game."""
        pygame.quit()
        raise SystemExit

    # endregion

    # endregion

    # region Game Loop

    def toggle_pause(self):
        """Toggle pause state."""
        self._paused = not self._paused

    def toggle_debug_overlay(self):
        """Toggle debug overlay display."""
        self._debug_overlay = not self._debug_overlay

    def reload_scene(self):
        """Reload the current scene."""
        SceneManager().reload_current()

    def main_loop(self) -> None:
        """Main game loop. Handles events, updates, and drawing."""

        while True:
            delta = self.__clock.tick(self._fps)

            self.__process_all_events()
            if not self._paused:
                self.pre_update(delta)
                self.__process_all_logic(delta)
                self.post_update(delta)
            self.pre_draw()
            self.__process_all_draw()
            self.post_draw()

    def __process_all_events(self) -> None:
        for event in pygame.event.get():

            SceneManager().current.handle_scene(event)
            self.__process_exit_events(event)

            if event.type == pygame.VIDEORESIZE:
                self._on_resize(event.size)

    def __process_all_logic(self, delta: float) -> None:
        SceneManager().current.update_scene(delta)

    def __process_all_draw(self) -> None:
        self.__screen.fill((255, 55, 23))
        self.__screen.blit(SceneManager().current.draw_scene(), (0, 0))
        if self._debug:
            if self._show_fps:
                fps = self.__clock.get_fps()
                fps_surf = self._font.render(f"FPS: {fps:.1f}", True, (0, 0, 0))
                self.__screen.blit(fps_surf, (10, 10))
            if self._debug_overlay:
                self._draw_debug_overlay()
        pygame.display.flip()

    def _draw_debug_overlay(self):
        """Draw debug info overlay."""
        info = [
            f"Paused: {self._paused}",
            f"Scene: {type(SceneManager().current).__name__}",
            f"Objects: {len(getattr(SceneManager().current, '_objects', []))}",
        ]
        for i, line in enumerate(info):
            surf = self._font.render(line, True, (0, 0, 0))
            self.__screen.blit(surf, (10, 30 + i * 20))

    def _on_resize(self, size):
        """Handle window resize event."""
        self._size = size
        self.__screen = pygame.display.set_mode(self._size, pygame.SCALED | pygame.RESIZABLE)
        if self._debug:
            print(f"Window resized to: {self._size}")

    # endregion

    # region Hooks

    def pre_update(self, delta: float):
        """Hook for logic before scene update."""

    def post_update(self, delta: float):
        """Hook for logic after scene update."""

    def pre_draw(self):
        """Hook for logic before drawing."""

    def post_draw(self):
        """Hook for logic after drawing."""

    # endregion

    # region Private

    def setup(self):
        """Load and register all scenes and objects before running the game."""
        import logging

        # 1. Register built-in objects and scenes
        try:
            import xodex.objects.objects
            import xodex.scenes.manager

            logging.info("Registered built-in objects and scenes.")
        except Exception as e:
            logging.error(f"Failed to register built-in objects/scenes: {e}")

        # 2. Register user/project objects and scenes if available
        try:
            # Try to import user project modules for registration
            game_module = import_module(self.game)
            try:
                # Try to import objects registration
                try:
                    import_path = f"{game_module.__name__}.objects.objects"
                    import_module(import_path)
                    logging.info(f"Registered user objects from {import_path}")
                except ImportError:
                    logging.warning("No user objects module found.")

                # Try to import scenes registration
                try:
                    import_path = f"{game_module.__name__}.scenes.scenes"
                    import_module(import_path)
                    logging.info(f"Registered user scenes from {import_path}")
                except ImportError:
                    logging.warning("No user scenes module found.")

            except Exception as e:
                logging.error(f"Error registering user objects/scenes: {e}")
        except Exception as e:
            logging.warning(f"No user game module found: {e}")

    # endregion
