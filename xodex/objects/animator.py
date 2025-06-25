"""Animator

Provides animation logic for a sequence of frames (Image or pygame.Surface).
Supports looping, ping-pong, reverse, and callbacks on finish.
"""

from typing import Callable, Optional, Tuple, List, Union
import pygame

from pygame import Surface

from xodex.objects.image import Image
from xodex.objects.objects import DrawableObject, EventfulObject, LogicalObject


class Animator(DrawableObject, EventfulObject, LogicalObject):
    """
    Handles frame-based animation logic.

    Args:
        frames (List[Surface]): List of animation frames.
        frame_duration (int): Duration of each frame in ms.
        loop (bool): Whether to loop the animation.
        pingpong (bool): Whether to ping-pong the animation.
        reverse (bool): Whether to play in reverse.
        on_finish (Optional[Callable]): Callback when animation finishes.

    Attributes:
        _frames (List[Surface]): Animation frames.
        _frame_duration (int): Duration per frame in ms.
        _current_frame (int): Current frame index.
        _time_accum (float): Accumulated time for frame switching.
        _loop (bool): Loop flag.
        _pingpong (bool): Ping-pong flag.
        _reverse (bool): Reverse flag.
        _on_finish (Optional[Callable]): Finish callback.
        _finished (bool): Animation finished flag.
        _direction (int): Animation direction (1 or -1).
    """

    def __init__(
        self,
        frames: List[Union[Image, Surface]],
        frame_duration: int = 100,
        loop: bool = True,
        pingpong: bool = False,
        reverse: bool = False,
        on_finish: Optional[Callable] = None,
        **kwargs,
    ):

        self._frames: List[Image] = []

        for frame in frames:
            if isinstance(frame, Surface):
                self._frames.append(Image(frame))
            elif isinstance(frame, Image):
                self._frames.append(frame)
            elif isinstance(frame, str):  # flappy
                self._frames.append(Image(frame))
            else:
                pass  # error

        self._frame_duration = frame_duration
        self._current_frame = 0
        self._time_accum = 0
        self._loop = loop
        self._pingpong = pingpong
        self._reverse = reverse
        self._on_finish = on_finish
        self._finished = False
        self._direction = -1 if reverse else 1
        self._img_rect = self._frames[self._current_frame].rect

        position = kwargs.pop("pos", None)
        if position:
            self._img_rect.x = position[0]
            self._img_rect.y = position[1]

    def __iter__(self):
        return iter(self._frames)

    def __contains__(self, frame: Image):
        return frame in self._frames

    def __bool__(self):
        return bool(self._frames)

    def __len__(self):
        """Return number of frames."""
        return len(self._frames)

    def __repr__(self):
        return f"<{self.__class__.__name__}({len(self)} frames)>"

    @property  # flappy
    def rect(self) -> pygame.Rect:
        """Get the (x, y) position of the image."""
        return self._img_rect

    @rect.setter  # flappy
    def rect(self, x: int, y: int, width: int, height: int):
        """Set the (x, y) position of the image."""
        self._img_rect = pygame.Rect(x, y, width, height)

    @property
    def position(self) -> Tuple[int, int]:
        """Get the (x, y) position of the image."""
        return (self._img_rect.x, self._img_rect.y)

    @position.setter
    def position(self, pos: Tuple[int, int]):
        """Set the (x, y) position of the image."""
        self._img_rect.x = pos[0]
        self._img_rect.y = pos[1]

    def reset(self):
        """Reset animation to start."""
        self._current_frame = 0 if self._direction == 1 else len(self._frames) - 1
        self._time_accum = 0
        self._finished = False

    def get_image(self) -> Optional[Image]:
        """Get the current frame's image."""
        if not self._frames:
            return None
        return self._frames[self._current_frame]

    def is_finished(self) -> bool:
        """Check if animation is finished."""
        return self._finished

    def set_reverse(self, reverse: bool = True):
        """Set animation to play in reverse."""
        self._reverse = reverse
        self._direction = -1 if reverse else 1

    def set_loop(self, loop: bool = True):
        """Enable or disable looping."""
        self._loop = loop

    def set_pingpong(self, pingpong: bool = True):
        """Enable or disable ping-pong mode."""
        self._pingpong = pingpong

    def set_on_finish(self, callback: Callable):
        """Set callback for when animation finishes."""
        self._on_finish = callback

    def set_frame_duration(self, duration: int):
        """Set duration per frame in ms."""
        self._frame_duration = duration

    def set_frame(self, frame_idx: int):
        """Set the current frame index."""
        if 0 <= frame_idx < len(self._frames):
            self._current_frame = frame_idx

    def get_frame(self) -> int:
        """Get the current frame index."""
        return self._current_frame

    def get_num_frames(self) -> int:
        """Get the total number of frames."""
        return len(self._frames)

    def set_frames(self, frames: List[Union[Image, Surface]]):
        """Set the animation frames and reset."""
        _frames = []
        for frame in frames:
            if isinstance(frame, Surface):
                _frames.append(Image(frame))
            elif isinstance(frame, Image):
                _frames.append(frame)
            else:
                pass
        self._frames = _frames
        self.reset()

    def set_speed(self, fps: int):
        """Set animation speed in frames per second."""
        self._frame_duration = int(1000 / fps)

    def play(self):
        """Resume animation."""
        self._finished = False

    def stop(self):
        """Pause animation."""
        self._finished = True

    def goto_and_play(self, frame_idx: int):
        """Jump to frame and play."""
        self.set_frame(frame_idx)
        self.play()

    def goto_and_stop(self, frame_idx: int):
        """Jump to frame and stop."""
        self.set_frame(frame_idx)
        self.stop()

    def perform_draw(self, surface: Surface, *args, **kwargs) -> None:
        """
        Draw the current frame onto a surface.

        Args:
            surface (Surface): The target surface.
        """
        image = self.get_image()
        image.rect = self.rect
        image.perform_draw(surface)

    def perform_update(self, deltatime: float, *args, **kwargs) -> None:
        """
        Update the animation state.

        Args:
            deltatime (float): Time since last update in ms.
        """
        if self._finished or len(self._frames) == 0:
            return
        self._time_accum += deltatime
        while self._time_accum >= self._frame_duration:
            self._time_accum -= self._frame_duration
            self._current_frame += self._direction
            if self._pingpong:
                if self._current_frame >= len(self._frames):
                    self._current_frame = len(self._frames) - 2
                    self._direction = -1
                elif self._current_frame < 0:
                    self._current_frame = 1
                    self._direction = 1
            else:
                if self._current_frame >= len(self._frames) or self._current_frame < 0:
                    if self._loop:
                        self._current_frame = 0 if self._direction == 1 else len(self._frames) - 1
                    else:
                        self._finished = True
                        if self._on_finish:
                            self._on_finish()
                        self._current_frame = max(0, min(self._current_frame, len(self._frames) - 1))

    def handle_event(self, event: pygame.event.Event, *args, **kwargs) -> None:
        """Handle pygame events (stub for extension)."""


class Anime(DrawableObject, LogicalObject, EventfulObject):  # dino
    """Anime"""

    def __init__(self, animation: dict[str, Animator] = None, default: str = None):
        self._animations: dict[str, Animator] = {}
        self._current: str = None

        if animation:
            if isinstance(animation, dict):
                self._animations.update(animation)
            else:
                raise TypeError
        if default:
            self._current = default

    def __str__(self):
        """Return a string representation of the Animator."""
        return f"<{self.__class__.__name__}>"

    def __repr__(self):
        """Return a string representation of the Animator."""
        return f"{self.__class__.__name__}()"

    @property
    def current(self) -> Animator:
        """Current Animator."""
        try:
            return self._animations[self._current]
        except KeyError:
            print("Current Animator is null")

    @current.setter
    def current(self, anime) -> str:
        """Current Animator."""
        if anime in self._animations:
            self._current = anime

    @property
    def animators(self):
        """Return Scen"""
        return self._animations

    @property  # flappy
    def rect(self) -> pygame.Rect:
        """Get or Set the rect of the anime."""
        return self.current.rect

    # @rect.setter  # flappy
    # def rect(self, new_rect: pygame.Rect):
    #     self.current.rect = new_rect

    @property
    def position(self) -> tuple[int, int]:
        """Get the (x, y) position of the anime."""
        return self.current.position

    @position.setter
    def position(self, pos: tuple[int, int]):
        self.current.position = pos

    def play(self, anime: str = None):
        """play"""
        if anime:
            self.current = anime

    def add(self, name: str, animator: Animator) -> None:
        """add"""
        self._animations[name] = animator

    def pop(self, name: str) -> None:
        """pop"""
        return self._animations.pop(name, None)

    def remove(self, name: str) -> None:
        """remove"""
        self.pop(name)

    def perform_draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        """
        Draw the current frame onto a surface.

        Args:
            surface (Surface): The target surface.
        """
        self.current.perform_draw(surface, *args, **kwargs)

    def perform_update(self, deltatime: float, *args, **kwargs) -> None:
        """
        Update the animation state.

        Args:
            deltatime (float): Time since last update in ms.
        """
        self.current.perform_update(deltatime, *args, **kwargs)

    def handle_event(self, event: pygame.event.Event, *args, **kwargs) -> None:
        """Handle pygame events (stub for extension)."""
        self.current.handle_event(event, *args, **kwargs)
