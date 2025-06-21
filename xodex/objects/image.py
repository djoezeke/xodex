"""Image

A wrapper for pygame.Surface that provides additional image manipulation
and drawing utilities, such as scaling, flipping, blurring, color swapping,
and rotation. Integrates with the DrawableObject interface for rendering.
"""

from typing import Tuple, Union, overload
import PIL.Image
import PIL.ImageFilter
import pygame
from pygame import Surface, Color

from xodex.objects.objects import DrawableObject
from xodex.utils.functions import loadimage


class Image(DrawableObject):
    """
    Image wrapper for pygame.Surface with utility methods.

    Args:
        image (Union[str, Surface], optional): Path to image file or a pygame.Surface.
        pos (Tuple[int, int], optional): Initial position (x, y) of the image.

    Attributes:
        _image (Surface): The underlying pygame surface.
        _img_rect (pygame.Rect): The rectangle representing the image's position and size.
    """

    @overload
    def __init__(self, image: Union[str, Surface] = None) -> None: ...

    def __init__(
        self, image: Union[str, Surface] = None, pos: Tuple[int, int] = (0, 0)
    ) -> None:
        if isinstance(image, str):
            self._image = loadimage(image)
        elif isinstance(image, Surface):
            self._image = image
        else:
            raise ValueError("Image must be initialized with a file path or pygame.Surface.")

        self._img_rect = self._image.get_rect()
        self._img_rect.x, self._img_rect.y = pos

    def __repr__(self):
        return f"<{self.__class__.__name__}({self._image})>"

    def __copy__(self) -> "Image":
        return Image(self._image)

    def __deepcopy__(self, memo) -> "Image":
        return Image(self._image)

    @property
    def image(self) -> Surface:
        """Return the underlying pygame.Surface."""
        return self._image

    @property
    def rect(self) -> pygame.Rect:
        """Return the pygame.Rect of the image."""
        return self._img_rect

    @property
    def position(self) -> Tuple[int, int]:
        """Get the (x, y) position of the image."""
        return (self._img_rect.x, self._img_rect.y)

    @position.setter
    def position(self, x: int, y: int):
        """Set the (x, y) position of the image."""
        self._img_rect.x = x
        self._img_rect.y = y

    def scale(self, x: float, y: float) -> "Image":
        """
        Scale the image to (x, y) size.

        Args:
            x (float): New width.
            y (float): New height.

        Returns:
            Image: Self for chaining.
        """
        self._image = pygame.transform.scale(self._image, (x, y))
        topleft = self._img_rect.topleft
        self._img_rect = self._image.get_rect()
        self._img_rect.topleft = topleft
        return self

    def smoothscale(self, x: float, y: float) -> "Image":
        """
        Smoothly scale the image to (x, y) size.

        Args:
            x (float): New width.
            y (float): New height.

        Returns:
            Image: Self for chaining.
        """
        self._image = pygame.transform.smoothscale(self._image, (x, y))
        topleft = self._img_rect.topleft
        self._img_rect = self._image.get_rect()
        self._img_rect.topleft = topleft
        return self

    def flip(self, flip_x: bool, flip_y: bool) -> "Image":
        """
        Flip the image horizontally and/or vertically.

        Args:
            flip_x (bool): Flip horizontally.
            flip_y (bool): Flip vertically.

        Returns:
            Image: Self for chaining.
        """
        self._image = pygame.transform.flip(self._image, flip_x, flip_y)
        topleft = self._img_rect.topleft
        self._img_rect = self._image.get_rect()
        self._img_rect.topleft = topleft
        return self

    def blur(self, blur_count: float = 5) -> "Image":
        """
        Apply a Gaussian blur to the image.

        Args:
            blur_count (float): Blur radius.

        Returns:
            Image: Self for chaining.
        """
        impil = PIL.Image.frombytes(
            "RGBA", self._img_rect.size, pygame.image.tobytes(self._image, "RGBA")
        )
        impil = impil.filter(PIL.ImageFilter.GaussianBlur(radius=blur_count))
        self._image = pygame.image.frombytes(
            impil.tobytes(), impil.size, "RGBA"
        ).convert()
        return self

    def swap_color(self, from_color: Color, to_color: Color) -> "Image":
        """
        Replace all pixels of a given color with another color.

        Args:
            from_color (Color): Color to replace.
            to_color (Color): Replacement color.

        Returns:
            Image: Self for chaining.
        """
        for x in range(self._image.get_width()):
            for y in range(self._image.get_height()):
                if self._image.get_at((x, y)) == from_color:
                    self._image.set_at((x, y), to_color)
        return self

    def rotate(self, angle: float) -> "Image":
        """
        Rotate the image by a given angle.

        Args:
            angle (float): Angle in degrees.

        Returns:
            Image: Self for chaining.
        """
        self._image = pygame.transform.rotate(self._image, angle)
        topleft = self._img_rect.topleft
        self._img_rect = self._image.get_rect()
        self._img_rect.topleft = topleft
        return self

    def perform_draw(self, surface: Surface, *args, **kwargs) -> None:
        """
        Draw the image onto a surface.

        Args:
            surface (Surface): The target surface.
        """
        surface.blit(self.image, self._img_rect)


# --- Main Demo ---
def main():
    """main"""
    running = True

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Image Demo")

    image = Image("custom/pyxox/pyxox/data/images/Background.png", (0, 0)).scale(800, 600)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 30, 30))
        # image.perform_draw(screen)
        screen.blit(image.image,(0,0))
        pygame.display.flip()


if __name__ == "__main__":
    main()
