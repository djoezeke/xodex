# from __future__ import annotations

# import os
# from unittest.mock import MagicMock

# import pytest


# @pytest.fixture
# def mock_settings_module(monkeypatch):
#     class Settings:
#         WINDOW_SIZE = (800, 600)
#         TITLE = "Test Game"
#         ICON_PATH = "icon.png"
#         FPS = 30
#         DEBUG = True
#         FULLSCREEN = False
#         MAIN_SCENE = "TestScene"
#         SHOW_FPS = True

#     monkeypatch.setattr(os, "environ", {})
#     return Settings


# @pytest.fixture
# def mock_pygame(monkeypatch):
#     # Patch pygame modules and methods
#     pygame_mock = MagicMock()
#     pygame_mock.SCALED = 1
#     pygame_mock.RESIZABLE = 2
#     pygame_mock.FULLSCREEN = 4
#     pygame_mock.font.SysFont.return_value = MagicMock()
#     pygame_mock.display.set_mode.return_value = MagicMock()
#     pygame_mock.display.set_caption = MagicMock()
#     pygame_mock.event.get.return_value = []
#     pygame_mock.time.Clock.return_value = MagicMock(get_fps=lambda: 60, tick=lambda x: 16)
#     monkeypatch.setitem(__import__("sys").modules, "pygame", pygame_mock)
#     monkeypatch.setitem(__import__("sys").modules, "pygame.font", pygame_mock.font)
#     monkeypatch.setitem(__import__("sys").modules, "pygame.display", pygame_mock.display)
#     monkeypatch.setitem(__import__("sys").modules, "pygame.event", pygame_mock.event)
#     monkeypatch.setitem(__import__("sys").modules, "pygame.time", pygame_mock.time)
#     return pygame_mock


# @pytest.fixture
# def mock_import_module(monkeypatch, mock_settings_module):
#     monkeypatch.setattr("importlib.import_module", lambda name: mock_settings_module())


# @pytest.fixture
# def mock_scene_manager(monkeypatch):
#     scene_mock = MagicMock()
#     scene_mock.get_scene.return_value = MagicMock(return_value=MagicMock())
#     scene_mock.current = MagicMock()
#     scene_mock.reset = MagicMock()
#     monkeypatch.setitem(
#         __import__("sys").modules, "xodex.scenes.manager", MagicMock(SceneManager=MagicMock(return_value=scene_mock))
#     )
#     return scene_mock


# def test_game_init(monkeypatch, mock_pygame, mock_import_module, mock_scene_manager):
#     from xodex.game.game import Game

#     g = Game("testgame")
#     assert g._size == (800, 600)
#     assert g._caption == "Test Game"
#     assert g._icon == "icon.png"
#     assert g._fps == 30
#     assert g._debug is True
#     assert g._fullscreen is False
#     assert g._mainscene == "TestScene"
#     assert g._show_fps is True
#     assert hasattr(g, "_font")
#     assert hasattr(g, "_debug_overlay")
#     assert hasattr(g, "_paused")
#     assert hasattr(g, "ready")
#     assert hasattr(g, "objects_ready")
#     assert hasattr(g, "scenes_ready")


# def test_toggle_pause(monkeypatch, mock_pygame, mock_import_module, mock_scene_manager):
#     from xodex.game.game import Game

#     g = Game("testgame")
#     prev = g._paused
#     g.toggle_pause()
#     assert g._paused != prev


# def test_debug_overlay(monkeypatch, mock_pygame, mock_import_module, mock_scene_manager):
#     from xodex.game.game import Game

#     g = Game("testgame")
#     prev_overlay = g._debug_overlay
#     g.toggle_debug_overlay()
#     assert g._debug_overlay != prev_overlay


# def test_on_resize(monkeypatch, mock_pygame, mock_import_module, mock_scene_manager):
#     from xodex.game.game import Game

#     g = Game("testgame")
#     g._on_resize((1024, 768))
#     assert g._size == (1024, 768)


# def test_exit_game(monkeypatch, mock_pygame, mock_import_module, mock_scene_manager):
#     from xodex.game.game import Game

#     g = Game("testgame")
#     with pytest.raises(SystemExit):
#         g.exit_game()


# if __name__ == "__main__":
#     pytest.main(["-v", "--tb=short", __file__])
#     # pytest.main(["-v", __file__], plugins=[mock_pygame])
