import os
from abc import ABC, abstractmethod
from importlib import import_module
from typing import Union,    Generator

import pygame
from pygame.event import Event

from xodex.objects import Objects,DrawableObject,EventfulObject,LogicalObject
from xodex.objects.manager import ObjectsManager

__all__ = ("BaseScene",)


class BaseScene(ABC):
    """BaseScene"""

    def __init__(self, *args, **kwargs) -> "BaseScene":
        self.setting = import_module(os.getenv("XODEX_SETTINGS_MODULE"))
        self._size = self.setting.WINDOW_SIZE or (560, 480)
        self._debug = self.setting.DEBUG or True
        self._start_time = pygame.time.get_ticks() / 1000
        self._screen = pygame.Surface(self._size)
        self._objects = Objects()

        self._object = ObjectsManager().get_objects()

    def __str__(self):
        """Return a string representation of the Scene."""
        return f"<{self.__class__.__name__} Scene> elapsed: {self.elapsed}"

    def __repr__(self):
        """Return a string representation of the widget."""
        return f"{self.__class__.__name__}()"

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

    @property
    def screen(self) -> pygame.Surface:
        """Return the Scene Surface"""
        return self._screen

    @property
    def object(self):
        """Return Object Manager"""
        return self._object

    def get_object(self, object_name: str)->Union[DrawableObject, EventfulObject, LogicalObject]:
        """Get an object."""
        return ObjectsManager().get_object(object_name=object_name)

    @property
    def size(self) -> tuple[int, int]:
        """Return the Scene Screen Size"""
        return self._size

    def draw_scene(self, *args, **kwargs) -> pygame.Surface:
        """draw"""
        self._screen.fill((255, 255, 255))
        self._objects.draw_object(self._screen, *args, **kwargs)
        return self._screen

    def update_scene(self, deltatime: float, *args, **kwargs) -> None:
        """update"""
        self._objects.update_object(deltatime, *args, **kwargs)

    def handle_scene(self, event: Event, *args, **kwargs) -> None:
        """handle"""
        if event.type == pygame.VIDEORESIZE:
            self._on_resize(event.size)
        self._objects.handle_object(event, *args, **kwargs)

    def setup(self):
        """setup"""
        self._objects.clear()
        if objects := self._generate_objects_():
            self._objects.extend(list(objects))

        if self._debug:
            print(self._objects)

    # endregion

    # region Hooks

    def on_enter(self, *args, **kwargs) -> None:
        """Runs When Enter the Scene"""

    def on_exit(self, *args, **kwargs) -> None:
        """Runs When Exit the Scene"""

    def on_first_enter(self, *args, **kwargs) -> None:
        """Run when First Time Playing Scene"""

    def on_last_exit(self, *args, **kwargs) -> None:
        """Run when Last Time Playing Scene"""

    # endregion
