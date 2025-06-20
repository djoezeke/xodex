from typing import Tuple, Optional,Dict

from xodex.utils.functions import splitsheet

class SpriteSheet:
    def __init__(self, image, frame_width, frame_height):
        self.image = image
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frames = splitsheet(image)

    def get_frame(self, i):
        return self.frames[i % len(self.frames)]
