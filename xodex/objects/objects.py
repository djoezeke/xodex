"""Objects

Defines base classes for game objects:
- LogicalObject: Updatable logic objects.
- DrawableObject: Renderable objects.
- EventfulObject: Objects that handle events.
"""

import time
from abc import ABC, abstractmethod

from pygame import Surface
from pygame.event import Event

__all__ = ("DrawableObject", "Object", "EventfulObject", "LogicalObject")


class Object:
    """Base class for all game objects."""


class LogicalObject(Object, ABC):
    """
    Abstract base class for logical (updatable) game objects.

    Inherit from this class and implement `perform_update` to define how the object updates its logic.
    Optionally, use `update_enabled` and `update_profile` for advanced update control.

    Provides a three-phase update process:
    - before_update: Pre-update hook (e.g., prepare state)
    - perform_update: Actual update logic (must be implemented)
    - after_update: Post-update hook (e.g., finalize state)

    Features:
    - Enable/disable updating at runtime.
    - Optional update profiling.
    - Update error handling hook.
    """

    update_enabled: bool = True  # Toggle updating on/off
    update_profile: bool = False  # Enable profiling of update time

    def update(self, deltatime: float, *args, **kwargs) -> None:
        """
        Update the instance.

        Args:
            deltatime (float): Time since last update in seconds.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        if not getattr(self, "update_enabled", True):
            return
        start_time = (
            time.perf_counter() if getattr(self, "update_profile", False) else None
        )
        try:
            self._before_update_(*args, **kwargs)
            self.perform_update(deltatime, *args, **kwargs)
            self._after_update_(*args, **kwargs)
        except Exception as exc:
            self.on_update_error(exc)
        finally:
            if start_time is not None:
                elapsed = time.perf_counter() - start_time
                self.on_update_profile(elapsed, *args, **kwargs)

    @abstractmethod
    def perform_update(self, deltatime: float, *args, **kwargs) -> None:
        """
        Actual update logic. Must be implemented by subclass.

        Args:
            deltatime (float): Time since last update in seconds.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        raise NotImplementedError("`perform_update()` must be implemented.")

    def enable_update(self) -> None:
        """Enable logic updates for this object."""
        self.update_enabled = True

    def disable_update(self) -> None:
        """Disable logic updates for this object."""
        self.update_enabled = False

    def _before_update_(self, *args, **kwargs) -> None:
        """Hook called before update. Override as needed."""

    def _after_update_(self, *args, **kwargs) -> None:
        """Hook called after update. Override as needed."""

    def on_update_profile(self, elapsed: float, *args, **kwargs) -> None:
        """
        Hook called with elapsed time if update_profile is enabled.

        Args:
            elapsed (float): Time in seconds spent in update().
        """
        # Override to log or collect update timing.

    def on_update_error(self, exc: Exception):
        """Hook called if an exception occurs during update."""
        # Override to log or handle update errors.


class DrawableObject(Object, ABC):
    """
    Abstract base class for drawable game objects.

    Inherit from this class and implement `perform_draw` to define how the object is rendered.
    Optionally, use `visible`  for advanced rendering control.

    Provides a three-phase draw process:
    - before_draw: Pre-draw hook (e.g., set up state)
    - perform_draw: Actual drawing logic (must be implemented)
    - after_draw: Post-draw hook (e.g., clean up state)

    Features:
    - Enable/disable drawing at runtime.
    - Optional draw profiling.
    - Draw error handling hook.
    - Supports visibility toggling.
    """

    visible: bool = True
    draw_enabled: bool = True  # Toggle drawing on/off
    draw_profile: bool = False  # Enable profiling of draw time

    def draw(self, surface: Surface, *args, **kwargs) -> None:
        """
        Draw the object if visible.

        Args:
            surface (Surface): The Pygame surface to draw on.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """

        if not getattr(self, "draw_enabled", True):
            return
        start_time = (
            time.perf_counter() if getattr(self, "draw_profile", False) else None
        )
        try:
            self._before_draw_(surface, *args, **kwargs)
            self.perform_draw(surface, *args, **kwargs)
            self._after_draw_(surface, *args, **kwargs)
        except Exception as exc:
            self.on_draw_error(exc)
        finally:
            if start_time is not None:
                elapsed = time.perf_counter() - start_time
                self.on_draw_profile(elapsed, surface, *args, **kwargs)

    @abstractmethod
    def perform_draw(self, surface: Surface, *args, **kwargs) -> None:
        """
        Actual drawing logic. Must be implemented by subclass.

        Args:
            surface (Surface): The Pygame surface to draw on.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        raise NotImplementedError("`perform_draw()` must be implemented.")

    def set_visible(self, visible: bool) -> None:
        """
        Set the visibility of the object.

        Args:
            visible (bool): If False, draw() will do nothing.
        """
        self.visible = visible

    def _before_draw_(self, surface: Surface, *args, **kwargs) -> None:
        """Hook called before drawing. Override as needed."""

    def _after_draw_(self, surface: Surface, *args, **kwargs) -> None:
        """Hook called after drawing. Override as needed."""

    def on_draw_profile(
        self, elapsed: float, surface: Surface, *args, **kwargs
    ) -> None:
        """
        Hook called with elapsed time if draw_profile is enabled.

        Args:
            elapsed (float): Time in seconds spent in draw().
            surface (Surface): The Pygame surface.
        """
        # Override to log or collect draw timing.

    def on_draw_error(self, exc: Exception):
        """Hook called if an exception occurs during draw."""
        # Override to log or handle draw errors.


class EventfulObject(Object, ABC):
    """
    Abstract base class for eventful game objects.

    Inherit from this class and implement `handle_event` to define how the object responds to events.
    Use event filters and handler binding for advanced event management.

    Provides a three-phase event process:
    - before_event: Pre-event hook (e.g., filter or preprocess event)
    - handle_event: Actual event handling logic (must be implemented)
    - after_event: Post-event hook (e.g., logging or cleanup)

    Features:
    - Supports binding multiple event handlers and event filtering.
    - Event type-based handler registry.
    - Optional event profiling and error handling.
    """

    event_profile: bool = False
    event_enabled: bool = True  # Toggle Interaction on/off

    def handle(self, event: Event, *args, **kwargs) -> None:
        """
        Handle an event.

        Args:
            event (Event): The Pygame event to handle.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        if not getattr(self, "event_enabled", True):
            return

        start_time = (
            time.perf_counter() if getattr(self, "event_profile", False) else None
        )
        try:
            self._before_event_(event, *args, **kwargs)
            self.handle_event(event, *args, **kwargs)
            self._after_event_(event, *args, **kwargs)
        except Exception as exc:
            self.on_event_error(exc)
        finally:
            if start_time is not None:
                elapsed = time.perf_counter() - start_time
                self.on_event_profile(elapsed, event, *args, **kwargs)

    @abstractmethod
    def handle_event(self, event: Event, *args, **kwargs) -> None:
        """
        Main event handler. Must be implemented by subclass.

        Args:
            event (Event): The Pygame event to handle.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        raise NotImplementedError("`handle_event()` must be implemented.")

    def _before_event_(self, event: Event, *args, **kwargs) -> None:
        """Hook called before event handling. Override as needed."""

    def _after_event_(self, event: Event, *args, **kwargs) -> None:
        """Hook called after event handling. Override as needed."""

    def on_event_profile(self, elapsed: float, event: Event, *args, **kwargs) -> None:
        """
        Hook called with elapsed time if event_profile is enabled.

        Args:
            elapsed (float): Time in seconds spent in event().
            event (Event): The event being handled.
        """
        # Override to log or collect event timing.

    def on_event_error(self, exc: Exception):
        """Hook called if an exception occurs during event handling."""
        # Override to log or handle event errors.

    def enable_event(self):
        """Enable the object for interaction."""
        self.event_enabled = True

    def disable_event(self):
        """Disable the object for interaction."""
        self.event_enabled = False
