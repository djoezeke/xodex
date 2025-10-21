import os
import sys

import pygame
import pytest

from xodex.conf import settings
from xodex.scene.base import BaseScene

# Mock settings module for testing


class MockSettings:
    WINDOW_SIZE = (800, 600)
    DEBUG = False


os.environ["XODEX_SETTINGS_MODULE"] = "mock_settings"

sys.modules["mock_settings"] = MockSettings
settings._setup()


# Concrete implementation for testing
class TestScene(BaseScene):
    def _generate_objects_(self):
        return []


def test_scene_initialization():
    scene = TestScene()
    assert scene.size == (800, 600)
    assert scene.get_background_color() == (255, 255, 255)
    assert not scene.is_paused
    assert isinstance(scene.screen, pygame.Surface)


def test_pause_resume_toggle():
    scene = TestScene()
    assert not scene.is_paused
    scene.pause()
    assert scene.is_paused
    scene.resume()
    assert not scene.is_paused
    scene.toggle_pause()
    assert scene.is_paused
    scene.toggle_pause()
    assert not scene.is_paused


def test_background_color_set_get():
    scene = TestScene()
    scene.set_background_color((100, 150, 200))
    assert scene.get_background_color() == (100, 150, 200)


# def test_lifecycle_hooks(monkeypatch):
#     scene = TestScene()
#     called = {}

#     monkeypatch.setattr(scene, "on_first_enter", lambda *a, **k: called.setdefault("first_enter", True))
#     monkeypatch.setattr(scene, "on_enter", lambda *a, **k: called.setdefault("enter", True))
#     monkeypatch.setattr(scene, "on_exit", lambda *a, **k: called.setdefault("exit", True))
#     monkeypatch.setattr(scene, "on_pause", lambda *a, **k: called.setdefault("pause", True))
#     monkeypatch.setattr(scene, "on_resume", lambda *a, **k: called.setdefault("resume", True))

#     # Simulate entering scene
#     scene.on_enter()
#     assert "first_enter" in called or "enter" in called

#     # Simulate pausing and resuming
#     scene.pause()
#     assert "pause" in called
#     scene.resume()
#     assert "resume" in called

#     # Simulate exiting scene
#     scene.on_exit()
#     assert "exit" in called


def test_draw_scene_and_update_scene():
    scene = TestScene()
    surf = scene.draw_scene()
    assert isinstance(surf, pygame.Surface)
    # Should not raise when updating
    scene.update_scene(0.016)


def test_handle_scene_resize_event():
    scene = TestScene()
    event = pygame.event.Event(pygame.VIDEORESIZE, size=(1024, 768))
    scene.handle_scene(event)
    assert scene.size == (1024, 768)


if __name__ == "__main__":
    pytest.main(["-v", "--tb=short", __file__])
