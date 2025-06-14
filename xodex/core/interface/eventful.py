"""Eventful base class for event-driven game objects.

Provides an abstract interface for objects that handle Pygame events.
Inherit from this class and implement `handle_event` to define custom event logic.

Features:
- Integrates with EventMixin for pre/post event hooks, error handling, profiling, and event filtering.
- Supports dynamic event handler binding and event type-based dispatch.
"""

from abc import ABC, abstractmethod
from pygame.event import Event
from .mixins import EventMixin


class Eventful(ABC, EventMixin):
    """
    Abstract base class for eventful game objects.

    Inherit from this class and implement `handle_event` to define how the object responds to events.
    Use event filters and handler binding for advanced event management.
    """

    def __init__(self):
        super().__init__()

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

    # Optional: Alias for compatibility with legacy code or typo
    def handel_event(self, event: Event, *args, **kwargs) -> None:
        """
        Deprecated alias for handle_event. Calls handle_event().
        """
        self.handle_event(event, *args, **kwargs)

    def set_event_profile(self, enabled: bool) -> None:
        """
        Enable or disable event profiling for this object.

        Args:
            enabled (bool): If True, event profiling is enabled.
        """
        self.event_profile = enabled

    def add_event_type_handler(self, event_type: int, handler):
        """
        Add a handler for a specific event type.

        Args:
            event_type (int): Pygame event type constant.
            handler (Callable): Function to handle the event.
        """
        self.bind_event_type_handler(event_type, handler)

    def remove_all_event_type_handlers(self):
        """
        Remove all event type-specific handlers.
        """
        self.unbind_all_event_type_handlers()

    def enable(self):
        """Enable the widget for interaction."""
        self._enabled = True

    def disable(self):
        """Disable the widget for interaction."""
        self._enabled = False
