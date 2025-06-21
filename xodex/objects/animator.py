"""SpriteSheet"""

from typing import overload
import pygame
from pygame import Surface
from xodex.objects.objects import DrawableObject,EventfulObject,LogicalObject

class Animator(DrawableObject,EventfulObject,LogicalObject):
    """Animator"""

    def __init__(
        self,
        frames: list[Surface],
        frame_duration=100,
        loop=True,
        pingpong=False,
        reverse=False,
        on_finish=None,
    ):
        self._frames: list[Surface] = frames  # list of surfaces
        self._frame_duration = frame_duration  # ms per frame
        self._current_frame = 0
        self._time_accum = 0
        self._loop = loop
        self._pingpong = pingpong
        self._reverse = reverse
        self._on_finish = on_finish
        self._finished = False
        self._direction = -1 if reverse else 1

    def __iter__(self):
        return iter(self._frames)

    def __contains__(self, frame):
        return frame in self._frames

    def __bool__(self):
        return bool(self._frames)

    def __len__(self):
        """return number of frames in sheet"""
        return len(self._frames)

    def __repr__(self):
        return f"<{self.__class__.__name__}({len(self)} frames)>"

    def reset(self):
        """reset"""
        self._current_frame = 0 if self._direction == 1 else len(self._frames) - 1
        self._time_accum = 0
        self._finished = False

    def get_image(self):
        """get_image"""
        if not self._frames:
            return None
        return self._frames[self._current_frame]

    def is_finished(self):
        """is_finished"""
        return self._finished

    def set_reverse(self, reverse=True):
        """set_reverse"""
        self._reverse = reverse
        self._direction = -1 if reverse else 1

    def set_loop(self, loop=True):
        """set_loop"""
        self._loop = loop

    def set_pingpong(self, pingpong=True):
        """set_pingpong"""
        self._pingpong = pingpong

    def set_on_finish(self, callback):
        """set_on_finish"""
        self._on_finish = callback

    def set_frame_duration(self, duration):
        """set_frame_duration"""
        self._frame_duration = duration

    def set_frame(self, frame_idx):
        """set_frame"""
        if 0 <= frame_idx < len(self._frames):
            self._current_frame = frame_idx

    def get_frame(self):
        """get_frame"""
        return self._current_frame

    def get_num_frames(self):
        """get_num_frames"""
        return len(self._frames)

    def set_frames(self, frames: list[Surface]):
        """set_frames"""
        self._frames = frames
        self.reset()

    def set_speed(self, fps: int):
        """set_speed"""
        self._frame_duration = int(1000 / fps)

    def play(self):
        """play"""
        self._finished = False

    def stop(self):
        """stop"""
        self._finished = True

    def goto_and_play(self, frame_idx):
        """goto_and_play"""
        self.set_frame(frame_idx)
        self.play()

    def goto_and_stop(self, frame_idx):
        """goto_and_stop"""
        self.set_frame(frame_idx)
        self.stop()

    def perform_draw(self, surface: Surface, *args, **kwargs) -> None:
        """perform_draw"""
        self.get_image().perform_draw(surface)

    def perform_update(self, deltatime: float, *args, **kwargs) -> None:
        """perform_update"""

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
                        self._current_frame = (
                            0 if self._direction == 1 else len(self._frames) - 1
                        )
                    else:
                        self._finished = True
                        if self._on_finish:
                            self._on_finish()
                        self._current_frame = max(
                            0, min(self._current_frame, len(self._frames) - 1)
                        )

    def handle_event(self, event: pygame.event.Event, *args, **kwargs) -> None:
        """handle_event"""
