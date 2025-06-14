"""Drawable base class for game objects.

Provides an abstract interface for objects that can be drawn on a Pygame surface.
Inherit from this class and implement `perform_draw` to define custom drawing logic.

Features:
- Integrates with DrawMixin for pre/post draw hooks, error handling, and profiling.
- Optionally supports visibility toggling and z-ordering for layered rendering.
"""

from abc import ABC, abstractmethod
from pygame.surface import Surface
from .mixins import DrawMixin


class Drawable(ABC, DrawMixin):
    """
    Abstract base class for drawable game objects.

    Inherit from this class and implement `perform_draw` to define how the object is rendered.
    Optionally, use `visible` and `z_index` for advanced rendering control.
    """

    visible: bool = True
    z_index: int = 0  # Used for sorting/layering drawables

    def draw(self, surface: Surface, *args, **kwargs) -> None:
        """
        Draw the object if visible.

        Args:
            surface (Surface): The Pygame surface to draw on.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        if not self.visible:
            return
        super().draw(surface, *args, **kwargs)

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

    def set_z_index(self, z: int) -> None:
        """
        Set the z-index (layer) for rendering order.

        Args:
            z (int): The z-index value.
        """
