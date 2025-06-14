import os
from abc import ABC, abstractmethod
from importlib import import_module
from typing import Generator, Callable

import pygame
from pygame.event import Event

from xodex.objects import Objects
from xodex.objects.manager import ObjectsManager

__all__ = ("BaseScene",)


class BaseScene(ABC):
    """BaseScene"""

    def __init__(self):
        self.setting = import_module(os.getenv("XODEX_SETTINGS_MODULE"))
        self._size = self.setting.WINDOW_SIZE or (560, 480)
        self._debug = self.setting.DEBUG or False

        self._start_time = pygame.time.get_ticks() / 1000
        self._screen = pygame.Surface(self._size)
        self._objects = Objects()

        self._on_enter_callbacks = []
        self._on_exit_callbacks = []
        self._on_update_callbacks = []
        self._on_draw_callbacks = []
        self.object = ObjectsManager()

    # region Private

    @abstractmethod
    def _generate_objects_(self) -> Generator:
        raise NotImplementedError

    def _on_resize(self, size):
        """Handle window resize event."""
        self._size = size
        self._screen = pygame.Surface(self._size)
        if self._debug:
            print(f"SceneWindow resized to: {self._size}")

    # endregion

    # region Public

    @property
    def elapsed(self) -> float:
        """Elapsed time since scene started (seconds)."""
        return pygame.time.get_ticks() / 1000 - self._start_time

    def draw(self) -> pygame.Surface:
        """draw"""
        self._screen.fill((0, 0, 0))
        for cb in self._on_draw_callbacks:
            cb(self._screen)
        self._objects.draw(self._screen)
        return self._screen

    def update(self, delta: float = 0.0) -> None:
        """update"""
        for cb in self._on_update_callbacks:
            cb(delta)
        self._objects.update(delta)

    def handle(self, event: Event) -> None:
        """handle"""
        if event.type == pygame.VIDEORESIZE:
            self._on_resize(event.size)
        self._objects.handle(event)

    def setup(self):
        """setup"""
        self._objects.clear()

        if obj := self._generate_objects_():
            self._objects.extend(list(obj))

        if self._debug:
            print(self._objects)

    def add_on_enter(self, callback: Callable):
        self._on_enter_callbacks.append(callback)

    def add_on_exit(self, callback: Callable):
        self._on_exit_callbacks.append(callback)

    def add_on_update(self, callback: Callable):
        self._on_update_callbacks.append(callback)

    def add_on_draw(self, callback: Callable):
        self._on_draw_callbacks.append(callback)

    def on_enter(self) -> None:
        for cb in self._on_enter_callbacks:
            cb()

    def on_exit(self) -> None:
        for cb in self._on_exit_callbacks:
            cb()

    def on_first_enter(self) -> None:
        pass

    def on_last_exit(self) -> None:
        pass

    # endregion
