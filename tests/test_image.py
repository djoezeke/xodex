# """Image Tests"""

# from unittest.mock import MagicMock
# from unittest.mock import patch

# import pygame
# import pytest
# from xodex.contrib.objects.image import Image


# @pytest.fixture
# def fake_surface():
#     surf = MagicMock(spec=pygame.Surface)
#     surf.get_rect.return_value = MagicMock(x=0, y=0, topleft=(0, 0), size=(10, 10))
#     surf.get_width.return_value = 10
#     surf.get_height.return_value = 10
#     surf.get_at.return_value = (255, 0, 0, 255)
#     return surf


# @patch(
#     "xodex.objects.image.loadimage",
#     return_value=MagicMock(
#         spec=pygame.Surface, get_rect=MagicMock(return_value=MagicMock(x=0, y=0, topleft=(0, 0), size=(10, 10)))
#     ),
# )
# def test_init_with_path(mock_loadimage):
#     img = Image("somefile.png")
#     assert img.image is mock_loadimage.return_value


# def test_init_with_surface(fake_surface):
#     img = Image(fake_surface)
#     assert img._image is fake_surface


# def test_position_and_rect(fake_surface):
#     img = Image(fake_surface)
#     img.pos((5, 7))
#     assert img.position == (5, 7)
#     rect = MagicMock()
#     img.rect = rect
#     assert img.rect is rect


# def test_pos_method(fake_surface):
#     img = Image(fake_surface)
#     img.pos((3, 4))
#     assert img.rect.x == 3
#     assert img.rect.y == 4


# @patch(
#     "pygame.transform.scale",
#     return_value=MagicMock(spec=pygame.Surface, get_rect=MagicMock(return_value=MagicMock(topleft=(0, 0)))),
# )
# def test_scale(mock_scale, fake_surface):
#     img = Image(fake_surface)
#     assert img.image.get_width() == 10
#     assert img.image.get_height() == 10
#     img.scale(20, 30)
#     mock_scale.assert_called_with(fake_surface, (20, 30))


# @patch(
#     "pygame.transform.smoothscale",
#     return_value=MagicMock(spec=pygame.Surface, get_rect=MagicMock(return_value=MagicMock(topleft=(0, 0)))),
# )
# def test_smoothscale(mock_smoothscale, fake_surface):
#     img = Image(fake_surface)
#     img.smoothscale(20, 30)
#     mock_smoothscale.assert_called_with(fake_surface, (20, 30))


# @patch(
#     "pygame.transform.flip",
#     return_value=MagicMock(spec=pygame.Surface, get_rect=MagicMock(return_value=MagicMock(topleft=(0, 0)))),
# )
# def test_flip(mock_flip, fake_surface):
#     img = Image(fake_surface)
#     img.flip(True, False)
#     mock_flip.assert_called_with(fake_surface, True, False)


# @patch("PIL.Image.frombytes")
# @patch("pygame.image.tobytes")
# @patch("pygame.image.frombytes")
# def test_blur(mock_frombytes, mock_tobytes, mock_frompil, fake_surface):
#     pil_img = MagicMock()
#     pil_img.filter.return_value = pil_img
#     pil_img.tobytes.return_value = b"123"
#     pil_img.size = (10, 10)
#     mock_frompil.return_value = pil_img
#     mock_frombytes.return_value = MagicMock(
#         spec=pygame.Surface, get_rect=MagicMock(return_value=MagicMock(topleft=(0, 0)))
#     )
#     img = Image(fake_surface)
#     img.blur(2)
#     assert mock_frombytes.called


# def test_swap_color(fake_surface):
#     img = Image(fake_surface)
#     fake_surface.get_width.return_value = 2
#     fake_surface.get_height.return_value = 2
#     fake_surface.get_at.return_value = (255, 0, 0, 255)
#     img.swap_color((255, 0, 0, 255), (0, 255, 0, 255))
#     assert fake_surface.set_at.call_count == 4


# @patch(
#     "pygame.transform.rotate",
#     return_value=MagicMock(spec=pygame.Surface, get_rect=MagicMock(return_value=MagicMock(topleft=(0, 0)))),
# )
# def test_rotate(mock_rotate, fake_surface):
#     img = Image(fake_surface)
#     img.rotate(90)
#     mock_rotate.assert_called_with(fake_surface, 90)


# def test_perform_draw(fake_surface):
#     img = Image(fake_surface)
#     surf = MagicMock()
#     img.perform_draw(surf)
#     surf.blit.assert_called_with(img.image, img._img_rect)


# if __name__ == "__main__":
#     pytest.main(["-v", "--tb=short", __file__])
