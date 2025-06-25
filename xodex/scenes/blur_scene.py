from abc import ABC
from typing import Callable, Optional
from PIL import Image, ImageFilter

import pygame
from pygame import Surface, time, image

from .base_scene import BaseScene

__all__ = ("BlurScene",)


class BlurScene(BaseScene, ABC):
    """BlurScene"""

    def __init__(
        self,
        blur_surface: Surface,
        *args,
        blur_count: int = 1,
        blur_duration: float = 1.0,
        on_blur_complete: Optional[Callable] = None,
        **kwargs,
    ) -> "BlurScene":
        super().__init__(*args, **kwargs)
        self._blur_count = blur_count
        self._blur_duration = blur_duration
        self._blur_finished = False
        self._on_blur_complete = on_blur_complete
        self._blur_surface = blur_surface

    def update_scene(self, deltatime: float, *args, **kwargs) -> None:
        """
        Update all objects in the scene, unless paused.

        Args:
            deltatime (float): Time since last update (ms).
        """
        if not self._blur_finished:
            blur_time = time.get_ticks() / 1000
            min_blur = min(
                (blur_time - self._start_time) * self._blur_count / self._blur_duration,
                self._blur_count,
            )
            self._blur_surface = self.blur(min_blur)
            self._blur_finished = min_blur == self._blur_count
            if self._blur_finished and self._on_blur_complete:
                self._on_blur_complete()
        super().update_scene(deltatime, *args, **kwargs)

    def draw_scene(self, *args, **kwargs) -> pygame.Surface:  # flappy
        """
        Draw all objects to the scene surface.

        Returns:
            pygame.Surface: The updated scene surface.
        """
        self._screen.blit(self._blur_surface, self._screen.get_rect())
        self._objects.draw_object(self._screen, *args, **kwargs)
        return self._screen

    def reset_blur(self):
        """Restart the blur effect."""
        self._start_time = time.get_ticks() / 1000
        self._blur_finished = False

    def is_blur_finished(self) -> bool:
        """Return True if bluring finished"""
        return self._blur_finished

    # region Private

    def blur(self, blur_count: int = 5) -> Surface:
        """blur a surface"""
        impil = Image.frombytes(
            "RGBA",
            self._blur_surface.get_size(),
            image.tostring(self._blur_surface, "RGBA"),
        )
        impil = impil.filter(ImageFilter.GaussianBlur(radius=blur_count))
        self._blur_surface = image.fromstring(impil.tobytes(), impil.size, "RGBA").convert()
        return self._blur_surface

    # endegion Private
