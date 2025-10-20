from __future__ import annotations

from abc import ABC
from abc import abstractmethod

import pygame
from pygame.event import Event

__all__ = ("SceneLayer",)


class BaseSceneLayer(ABC):
    @abstractmethod
    def draw_layer(self, *args, **kwargs) -> pygame.Surface:
        """
        Draw layer to the scene surface.

        Returns:
            pygame.Surface: The updated scene surface.
        """

    @abstractmethod
    def update_layer(self, deltatime: float, *args, **kwargs) -> None:
        """
        Update all objects in layer.

        Args:
            deltatime (float): Time since last update (ms).
        """

    @abstractmethod
    def handle_layer(self, event: Event, *args, **kwargs) -> None:
        """
        Handle an event for all objects in the layer.

        Args:
            event (pygame.event.Event): The event to handle.
        """

    # def on_attach(self, *args, **kwargs) -> None:
    #     """
    #     Runs when the layer is attached.
    #     Override in subclasses for custom behavior.
    #     """

    # def on_detach(self, *args, **kwargs) -> None:
    #     """
    #     Runs when detaching the layer.
    #     Override in subclasses for custom behavior.
    #    """


class SceneLayer(BaseSceneLayer):
    pass
