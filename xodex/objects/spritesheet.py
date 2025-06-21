from typing import Tuple,Union ,overload

import pygame
from xodex.objects.image import Image
from xodex.utils.functions import splitsheet

class SpriteSheet:

    @overload
    def __init__(self, image:Union[str,pygame.Surface],frame_width:int=64, frame_height:int=80,num_frames:int=None):
        self._frames = [Image(image) for image in splitsheet(image,num_frames,(frame_width,frame_height))]

    def __init__(self, image:Union[str,pygame.Surface],frame_size:Tuple[int,int]=(64,80),num_frames:int =None):
        self._frames = [Image(image) for image in splitsheet(image,frame_size,num_frames)]

    def __call__(self):
        return iter(self._frames)

    def __iter__(self):
        return iter(self._frames)

    def __setitem__(self, frame_idx: int, frame:Image):
        if frame_idx > len(self):
            raise IndexError
        self._frames[frame_idx] = frame

    def __getitem__(self, frame_idx: int):
        if frame_idx > len(self):
            raise IndexError
        return self._frames[frame_idx]

    def __delitem__(self, frame_idx: int):
        if frame_idx > len(self):
            raise IndexError
        return self._frames.pop(frame_idx)

    def __contains__(self, frame):
        return frame in self._frames

    def __bool__(self) -> bool:
        return bool(self._frames)

    def __len__(self) -> int:
        return len(self._frames)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({len(self)} frames)>"

    def get_frame(self, i):
        return self.frames[i % len(self.frames)]

    def addframe(
        self,
        sheet: Union[str, pygame.Surface],
        frame_width: int = 64,
        frame_height: int = 80,
        num_frames: int = 1,
    ):
        """addframe"""
        new_sheet = SpriteSheet(sheet, frame_width, frame_height,num_frames)
        frames = new_sheet.frames()
        self._frames.append(frames)

    def removeframe(self, frame_idx: int) -> Image:
        """getframe"""
        return self.frames().pop(frame_idx)

    def getframe(self, frame_idx: int) -> Image:
        """getframe"""
        return self.frames()[frame_idx]

    def getimage(self, frame_idx: int) -> pygame.Surface:
        """getimage"""
        return self.images()[frame_idx]

    def frames(self) -> list[Image]:
        """image"""
        return self._frames

    def images(self) -> list[pygame.Surface]:
        """image"""
        return [frame.image for frame in self._frames]

