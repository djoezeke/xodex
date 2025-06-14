"""Logical base class for updatable game objects.

Provides an abstract interface for objects that require logic updates each frame.
Inherit from this class and implement `perform_update` to define custom update logic.

Features:
- Integrates with UpdateMixin for pre/post update hooks, error handling, and profiling.
- Supports enabling/disabling updates at runtime.
- Optionally supports update priorities for ordered logic execution.
"""

from abc import ABC, abstractmethod
from .mixins import UpdateMixin


class Logical(ABC, UpdateMixin):
    """
    Abstract base class for logical (updatable) game objects.

    Inherit from this class and implement `perform_update` to define how the object updates its logic.
    Optionally, use `update_enabled` and `update_priority` for advanced update control.
    """

    update_priority: int = 0  # Used for sorting/prioritizing logic updates

    @abstractmethod
    def perform_update(self, *args, **kwargs) -> None:
        """
        Actual update logic. Must be implemented by subclass.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        raise NotImplementedError("`perform_update()` must be implemented.")

    def set_update_priority(self, priority: int) -> None:
        """
        Set the update priority for this object.

        Args:
            priority (int): The update priority value (higher runs later if sorted).
        """
        self.update_priority = priority

    def enable_update(self) -> None:
        """
        Enable logic updates for this object.
        """
        self.update_enabled = True

    def disable_update(self) -> None:
        """
        Disable logic updates for this object.
        """
        self.update_enabled = False
