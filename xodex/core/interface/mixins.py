"""Mixins for game object behaviors.

These mixins provide reusable hooks for drawing, updating, and event handling.
They are designed to be inherited by game objects to add modular functionality.

Features:
- Enable/disable drawing and updating at runtime.
- Pre/post hooks for draw, update, and event handling.
- Event filtering and multiple event handler support.
- Optional profiling and error handling hooks.
"""

from typing import Callable, Any, List, Dict
from pygame.surface import Surface
from pygame.event import Event
import time


class DrawMixin:
    """
    Mixin to add drawing capability to an object.

    Provides a three-phase draw process:
    - before_draw: Pre-draw hook (e.g., set up state)
    - perform_draw: Actual drawing logic (must be implemented)
    - after_draw: Post-draw hook (e.g., clean up state)

    Features:
    - Enable/disable drawing at runtime.
    - Optional draw profiling.
    - Draw error handling hook.
    """

    draw_enabled: bool = True  # Toggle drawing on/off
    draw_profile: bool = False  # Enable profiling of draw time

    def draw(self, surface: Surface, *args, **kwargs) -> None:
        """
        Draw the instance on the given surface.

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
            self.before_draw(surface, *args, **kwargs)
            self.perform_draw(surface, *args, **kwargs)
            self.after_draw(surface, *args, **kwargs)
        except Exception as e:
            self.on_draw_error(e, surface, *args, **kwargs)
        finally:
            if start_time is not None:
                elapsed = time.perf_counter() - start_time
                self.on_draw_profile(elapsed, surface, *args, **kwargs)

    def before_draw(self, surface: Surface, *args, **kwargs) -> None:
        """
        Hook called before drawing. Override as needed.
        """
        pass

    def perform_draw(self, surface: Surface, *args, **kwargs) -> None:
        """
        Actual drawing logic. Must be implemented by subclass.
        """
        raise NotImplementedError("perform_draw must be implemented by subclass.")

    def after_draw(self, surface: Surface, *args, **kwargs) -> None:
        """
        Hook called after drawing. Override as needed.
        """
        pass

    def set_draw_enabled(self, enabled: bool) -> None:
        """
        Enable or disable drawing for this object.

        Args:
            enabled (bool): If False, draw() will do nothing.
        """
        self.draw_enabled = enabled

    def on_draw_error(
        self, error: Exception, surface: Surface, *args, **kwargs
    ) -> None:
        """
        Hook called if an exception occurs during drawing.

        Args:
            error (Exception): The exception raised.
            surface (Surface): The Pygame surface.
        """
        raise error  # By default, re-raise. Override for custom handling.

    def on_draw_profile(
        self, elapsed: float, surface: Surface, *args, **kwargs
    ) -> None:
        """
        Hook called with elapsed time if draw_profile is enabled.

        Args:
            elapsed (float): Time in seconds spent in draw().
            surface (Surface): The Pygame surface.
        """
        pass  # Override to log or collect draw timing.


class UpdateMixin:
    """
    Mixin to add update capability to an object.

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

    def update(self, *args, **kwargs) -> None:
        """
        Update the instance.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        if not getattr(self, "update_enabled", True):
            return
        start_time = (
            time.perf_counter() if getattr(self, "update_profile", False) else None
        )
        try:
            self.before_update(*args, **kwargs)
            self.perform_update(*args, **kwargs)
            self.after_update(*args, **kwargs)
        except Exception as e:
            self.on_update_error(e, *args, **kwargs)
        finally:
            if start_time is not None:
                elapsed = time.perf_counter() - start_time
                self.on_update_profile(elapsed, *args, **kwargs)

    def before_update(self, *args, **kwargs) -> None:
        """
        Hook called before update. Override as needed.
        """
        pass

    def perform_update(self, *args, **kwargs) -> None:
        """
        Actual update logic. Must be implemented by subclass.
        """
        raise NotImplementedError("perform_update must be implemented by subclass.")

    def after_update(self, *args, **kwargs) -> None:
        """
        Hook called after update. Override as needed.
        """
        pass

    def set_update_enabled(self, enabled: bool) -> None:
        """
        Enable or disable updating for this object.

        Args:
            enabled (bool): If False, update() will do nothing.
        """
        self.update_enabled = enabled

    def on_update_error(self, error: Exception, *args, **kwargs) -> None:
        """
        Hook called if an exception occurs during updating.

        Args:
            error (Exception): The exception raised.
        """
        raise error  # By default, re-raise. Override for custom handling.

    def on_update_profile(self, elapsed: float, *args, **kwargs) -> None:
        """
        Hook called with elapsed time if update_profile is enabled.

        Args:
            elapsed (float): Time in seconds spent in update().
        """
        pass  # Override to log or collect update timing.


class EventMixin:
    """
    Mixin to add event handling capability to an object.

    Provides a three-phase event process:
    - before_event: Pre-event hook (e.g., filter or preprocess event)
    - handle_event: Actual event handling logic (must be implemented)
    - after_event: Post-event hook (e.g., logging or cleanup)

    Features:
    - Supports binding multiple event handlers and event filtering.
    - Event type-based handler registry.
    - Optional event profiling and error handling.
    """

    def __init__(self):
        self._event_handlers: List[Callable[[Event, Any], None]] = []
        self._event_filters: List[Callable[[Event], bool]] = []
        self._event_type_handlers: Dict[int, List[Callable[[Event, Any], None]]] = {}
        self.event_profile: bool = False

    def event(self, event: Event, *args, **kwargs) -> None:
        """
        Handle an event.

        Args:
            event (Event): The Pygame event to handle.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        if not self._passes_event_filters(event):
            return
        start_time = (
            time.perf_counter() if getattr(self, "event_profile", False) else None
        )
        try:
            self.before_event(event, *args, **kwargs)
            self.handle_event(event, *args, **kwargs)
            # Call type-specific handlers
            for handler in self._event_type_handlers.get(event.type, []):
                handler(event, *args, **kwargs)
            # Call generic handlers
            for handler in self._event_handlers:
                handler(event, *args, **kwargs)
            self.after_event(event, *args, **kwargs)
        except Exception as e:
            self.on_event_error(e, event, *args, **kwargs)
        finally:
            if start_time is not None:
                elapsed = time.perf_counter() - start_time
                self.on_event_profile(elapsed, event, *args, **kwargs)

    def before_event(self, event: Event, *args, **kwargs) -> None:
        """
        Hook called before event handling. Override as needed.
        """
        pass

    def handle_event(self, event: Event, *args, **kwargs) -> None:
        """
        Actual event handling logic. Must be implemented by subclass.
        """
        raise NotImplementedError("handle_event must be implemented by subclass.")

    def after_event(self, event: Event, *args, **kwargs) -> None:
        """
        Hook called after event handling. Override as needed.
        """
        pass

    def bind_event_handler(self, handler: Callable[[Event, Any], None]) -> None:
        """
        Bind a custom event handler. Multiple handlers can be registered.

        Args:
            handler (Callable): Function to handle events.
        """
        self._event_handlers.append(handler)

    def bind_event_type_handler(
        self, event_type: int, handler: Callable[[Event, Any], None]
    ) -> None:
        """
        Bind a handler for a specific event type.

        Args:
            event_type (int): Pygame event type constant.
            handler (Callable): Function to handle the event.
        """
        if event_type not in self._event_type_handlers:
            self._event_type_handlers[event_type] = []
        self._event_type_handlers[event_type].append(handler)

    def clear_event_handlers(self) -> None:
        """
        Remove all custom event handlers.
        """
        self._event_handlers.clear()
        self._event_type_handlers.clear()

    def add_event_filter(self, filter_func: Callable[[Event], bool]) -> None:
        """
        Add a filter function to determine if an event should be handled.

        Args:
            filter_func (Callable): Function that returns True if event should be handled.
        """
        self._event_filters.append(filter_func)

    def clear_event_filters(self) -> None:
        """
        Remove all event filters.
        """
        self._event_filters.clear()

    def _passes_event_filters(self, event: Event) -> bool:
        """
        Check if the event passes all filters.

        Args:
            event (Event): The event to check.

        Returns:
            bool: True if all filters pass, False otherwise.
        """
        for filter_func in self._event_filters:
            if not filter_func(event):
                return False
        return True

    def on_event_error(self, error: Exception, event: Event, *args, **kwargs) -> None:
        """
        Hook called if an exception occurs during event handling.

        Args:
            error (Exception): The exception raised.
            event (Event): The event being handled.
        """
        raise error  # By default, re-raise. Override for custom handling.

    def on_event_profile(self, elapsed: float, event: Event, *args, **kwargs) -> None:
        """
        Hook called with elapsed time if event_profile is enabled.

        Args:
            elapsed (float): Time in seconds spent in event().
            event (Event): The event being handled.
        """
        pass  # Override to log or collect event timing.
