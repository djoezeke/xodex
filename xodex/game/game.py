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

    def __init__(self, *args, game: str = "", **kwargs) -> None:

        # Full Python path to the game event.g. 'hello.hello'.
        self.game = game

        pygame.init()

        if game:
            os.environ.setdefault("XODEX_SETTINGS_MODULE", f"{game}.settings")

        xodex_settings = os.getenv("XODEX_SETTINGS_MODULE")

        self.setting = import_module(xodex_settings)  # TODO Fix import Error in build

        self._size = self.setting.WINDOW_SIZE or (560, 480)
        self._caption = self.setting.TITLE or "Xodex"
        self._icon = self.setting.ICON_PATH or "Xodex"
        self.__fps = self.setting.FPS or 60
        self._debug = self.setting.DEBUG or False
        self._fullscreen = self.setting.FULLSCREEN or False
        self._mainscene = self.setting.MAIN_SCENE or "XodexMainScene"

        self.__screen = pygame.display.set_mode(
            self._size, pygame.SCALED | pygame.RESIZABLE
        )

        if self._fullscreen:
            self.__screen = pygame.display.set_mode(
                self._size, pygame.SCALED | pygame.RESIZABLE | pygame.FULLSCREEN
            )

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

    def main_loop(self) -> None:
        """Main game loop. Handles events, updates, and drawing."""

        while True:
            delta = self.__clock.tick(self.__fps) / 1000.0

            self.__process_all_events()
            self.__process_all_logic(delta)
            self.__process_all_draw()

    def __process_all_events(self) -> None:
        for event in pygame.event.get():

            SceneManager().current.handle(event)
            self.__process_exit_events(event)

            if event.type == pygame.VIDEORESIZE:
                self._on_resize(event.size)

    def __process_all_logic(self, delta: float = 0.0) -> None:
        SceneManager().current.update(delta)

    def __process_all_draw(self) -> None:
        self.__screen.fill((255, 55, 23))
        self.__screen.blit(SceneManager().current.draw(), (0, 0))
        # self._draw_debug_overlay()
        pygame.display.flip()

    def _on_resize(self, size):
        """Handle window resize event."""
        self._size = size
        self.__screen = pygame.display.set_mode(
            self._size, pygame.SCALED | pygame.RESIZABLE
        )
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
        """Load registered scenes and objects."""
        game_module = None

        try:
            game_module = import_module(self.game)
        except Exception:
            pass
        else:
            try:
                objects_module = (
                    game_module.__path__
                    + "."
                    + game_module.__name__
                    + OBJECTS_MODULE_NAME
                )
                try:
                    objects_module = import_module(objects_module)
                except ImportError:
                    pass  # Improperly Configured

                scenes_module = (
                    game_module.__path__
                    + "."
                    + game_module.__name__
                    + SCENES_MODULE_NAME
                )
                try:
                    scenes_module = import_module(scenes_module)
                except ImportError:
                    pass  # Improperly Configured
            finally:
                pass

    # endregion
