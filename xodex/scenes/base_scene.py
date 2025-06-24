import os
from abc import ABC, abstractmethod
from importlib import import_module
from typing import Union, Generator, Optional, Any

import pygame
from pygame.event import Event

from xodex.objects import Objects, DrawableObject, EventfulObject, LogicalObject
from xodex.objects.manager import ObjectsManager

__all__ = ("BaseScene",)


class BaseScene(ABC):
    """
    Abstract base class for all scenes in the Xodex engine.

    Provides a standard interface and utility methods for scene management,
    including object handling, drawing, updating, event processing, and lifecycle hooks.

    Attributes:
        setting: The imported settings module (from XODEX_SETTINGS_MODULE).
        _size (tuple[int, int]): The window size for the scene.
        _debug (bool): Debug mode flag.
        _start_time (float): Time when the scene was created (seconds).
        _screen (pygame.Surface): The surface representing the scene.
        _objects (Objects): The collection of drawable/eventful/logical objects.
        _object: The global object manager's objects.
        _paused (bool): Whether the scene is currently paused.
        _background_color (tuple[int, int, int]): Background color for the scene.

    Methods:
        elapsed: Elapsed time since scene started (seconds).
        screen: Returns the scene's surface.
        object: Returns the object manager's objects.
        get_object(object_name): Get an object by name from the manager.
        size: Returns the scene's window size.
        draw_scene: Draw all objects to the scene surface.
        update_scene: Update all objects in the scene.
        handle_scene: Handle an event for all objects.
        setup: Clear and regenerate scene objects.
        pause/resume/toggle_pause: Control scene pause state.
        is_paused: Check if the scene is paused.
        set_background_color: Set the background color.
        get_background_color: Get the background color.
        on_enter/on_exit/on_first_enter/on_last_exit/on_pause/on_resume: Scene lifecycle hooks.
    """

    def __init__(self, *args, **kwargs) -> "BaseScene":
        """
        Initialize the scene, loading settings and preparing the surface and objects.
        """
        self.setting = import_module(os.getenv("XODEX_SETTINGS_MODULE"))
        self._size = getattr(self.setting, "WINDOW_SIZE", (560, 480)) or (560, 480)
        self._debug = getattr(self.setting, "DEBUG", True)
        self._start_time = pygame.time.get_ticks() / 1000
        self._screen = pygame.Surface(self._size)
        self._object = ObjectsManager().get_objects()
        self._objects = Objects()
        self._paused = False
        self._background_color = getattr(self.setting, "BACKGROUND_COLOR", (255, 255, 255))
        self._first_entered = False

    def __str__(self):
        """Return a string representation of the Scene."""
        return f"<{self.__class__.__name__} Scene> elapsed: {self.elapsed:.2f}s paused: {self._paused}"

    def __repr__(self):
        """Return a string representation of the widget."""
        return f"{self.__class__.__name__}()"

    # region Private

    @abstractmethod
    def _generate_objects_(self) -> Generator:
        """
        Abstract method to generate scene objects.
        Should yield or return objects to be added to the scene.
        """
        raise NotImplementedError

    def _on_resize(self, size):
        """
        Handle window resize event.

        Args:
            size (tuple[int, int]): New window size.
        """
        self._size = size
        self._screen = pygame.Surface(self._size)
        if self._debug:
            print(f"SceneWindow resized to: {self._size}")

    # endregion

    # region Public

    @property
    def elapsed(self) -> float:
        """
        Elapsed time since scene started (seconds).

        Returns:
            float: Seconds since scene was created.
        """
        return pygame.time.get_ticks() / 1000 - self._start_time

    @property
    def screen(self) -> pygame.Surface:
        """
        Return the Scene Surface.

        Returns:
            pygame.Surface: The surface for this scene.
        """
        return self._screen

    @property
    def object(self):
        """
        Return Object Manager's objects.

        Returns:
            Any: The objects managed by the global ObjectsManager.
        """
        return self._object

    def get_object(self, object_name: str) -> Union[DrawableObject, EventfulObject, LogicalObject, None]:
        """
        Get an object by name from the global object manager.

        Args:
            object_name (str): The name of the object.

        Returns:
            DrawableObject | EventfulObject | LogicalObject | None: The requested object, or None if not found.
        """
        return ObjectsManager().get_object(object_name=object_name)

    @property
    def size(self) -> tuple[int, int]:
        """
        Return the Scene Screen Size.

        Returns:
            tuple[int, int]: The (width, height) of the scene.
        """
        return self._size

    def draw_scene(self, *args, **kwargs) -> pygame.Surface:
        """
        Draw all objects to the scene surface.

        Returns:
            pygame.Surface: The updated scene surface.
        """
        self._screen.fill(self._background_color)
        self._objects.draw_object(self._screen, *args, **kwargs)
        return self._screen

    def update_scene(self, deltatime: float, *args, **kwargs) -> None:
        """
        Update all objects in the scene, unless paused.

        Args:
            deltatime (float): Time since last update (ms).
        """
        if not self._paused:
            self._objects.update_object(deltatime, *args, **kwargs)

    def handle_scene(self, event: Event, *args, **kwargs) -> None:
        """
        Handle an event for all objects in the scene.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        if event.type == pygame.VIDEORESIZE:
            self._on_resize(event.size)
        if not self._paused:
            self._objects.handle_object(event, *args, **kwargs)

    def setup(self):
        """
        Clear and regenerate scene objects by calling _generate_objects_.
        """
        self._objects.clear()
        if objects := self._generate_objects_():
            self._objects.extend(list(objects))
        if self._debug:
            print(f"[{self.__class__.__name__}] Objects after setup: {self._objects}")

    # --- New Features ---

    def pause(self):
        """Pause the scene (updates and event handling will be skipped)."""
        if not self._paused:
            self._paused = True
            self.on_pause()
            if self._debug:
                print(f"[{self.__class__.__name__}] Scene paused.")

    def resume(self):
        """Resume the scene (updates and event handling will continue)."""
        if self._paused:
            self._paused = False
            self.on_resume()
            if self._debug:
                print(f"[{self.__class__.__name__}] Scene resumed.")

    def toggle_pause(self):
        """Toggle the pause state of the scene."""
        if self._paused:
            self.resume()
        else:
            self.pause()

    @property
    def is_paused(self) -> bool:
        """Return whether the scene is currently paused."""
        return self._paused

    def set_background_color(self, color: tuple[int, int, int]):
        """
        Set the background color for the scene.

        Args:
            color (tuple[int, int, int]): RGB color.
        """
        self._background_color = color
        if self._debug:
            print(f"[{self.__class__.__name__}] Background color set to: {self._background_color}")

    def get_background_color(self) -> tuple[int, int, int]:
        """
        Get the current background color.

        Returns:
            tuple[int, int, int]: The RGB color.
        """
        return self._background_color

    # endregion

    # region Hooks

    def on_enter(self, *args, **kwargs) -> None:
        """
        Runs when entering the scene.
        Override in subclasses for custom behavior.
        """
        if not self._first_entered:
            self.on_first_enter(*args, **kwargs)
            self._first_entered = True
        if self._debug:
            print(f"[{self.__class__.__name__}] on_enter called.")

    def on_exit(self, *args, **kwargs) -> None:
        """
        Runs when exiting the scene.
        Override in subclasses for custom behavior.
        """
        if self._debug:
            print(f"[{self.__class__.__name__}] on_exit called.")

    def on_first_enter(self, *args, **kwargs) -> None:
        """
        Runs the first time the scene is entered.
        Override in subclasses for custom behavior.
        """
        if self._debug:
            print(f"[{self.__class__.__name__}] on_first_enter called.")

    def on_last_exit(self, *args, **kwargs) -> None:
        """
        Runs the last time the scene is exited.
        Override in subclasses for custom behavior.
        """
        if self._debug:
            print(f"[{self.__class__.__name__}] on_last_exit called.")

    def on_pause(self, *args, **kwargs) -> None:
        """
        Runs when the scene is paused.
        Override in subclasses for custom behavior.
        """
        if self._debug:
            print(f"[{self.__class__.__name__}] on_pause called.")

    def on_resume(self, *args, **kwargs) -> None:
        """
        Runs when the scene is resumed from pause.
        Override in subclasses for custom behavior.
        """
        if self._debug:
            print(f"[{self.__class__.__name__}] on_resume called.")

    # endregion
