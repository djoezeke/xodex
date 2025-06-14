from abc import ABC
from typing import Callable, Optional

from pygame import Surface, time

from .base_scene import BaseScene

__all__ = ("BlurScene",)


class BlurScene(BaseScene, ABC):
    """BlurScene"""

    def __init__(
        self,
        blur_surface: Surface,
        blur_count: int = 1,
        blur_duration: float = 1.0,
        on_blur_complete: Optional[Callable] = None,
    ):
        super().__init__()
        self._blur_count = blur_count
        self._blur_duration = blur_duration
        self._blur_finished = False
        self._on_blur_complete = on_blur_complete
        # self._blur_surface = ImgObj(copy(blur_surface), (0, 0))

    def update(self, delta: float = 0.0) -> None:
        if not self._blur_finished:
            blur_time = time.get_ticks() / 1000
            min_blur = min(
                (blur_time - self._start_time) * self._blur_count / self._blur_duration,
                self._blur_count,
            )
            # self._blur_surface.blur(min_blur)
            self._blur_finished = min_blur == self._blur_count
            if self._blur_finished and self._on_blur_complete:
                self._on_blur_complete()
        super().update(delta)

    def draw(self) -> Surface:
        # self._blur_surface.draw(self._screen)
        self._objects.draw(self._screen)
        return self._screen

    def reset_blur(self):
        """Restart the blur effect."""
        self._start_time = time.get_ticks() / 1000
        self._blur_finished = False

    def is_blur_finished(self) -> bool:
        """Return True if bluring finished"""
        return self._blur_finished
