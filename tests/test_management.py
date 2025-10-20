# from unittest.mock import MagicMock

# import pytest
# from xodex.core.management import ManagementUtility


# @pytest.fixture
# def mock_game(monkeypatch):
#     game_mock = MagicMock()
#     monkeypatch.setitem(__import__("sys").modules, "xodex.game.game", MagicMock(Game=MagicMock(return_value=game_mock)))
#     return game_mock


# @pytest.fixture
# def mock_project_builder(monkeypatch):
#     builder_mock = MagicMock()
#     monkeypatch.setitem(__import__("sys").modules, "xodex.core.management.ProjectBuilder", builder_mock)
#     return builder_mock


# @pytest.fixture
# def mock_project_generator(monkeypatch):
#     generator_mock = MagicMock()
#     monkeypatch.setitem(__import__("sys").modules, "xodex.core.management.ProjectGenerator", generator_mock)
#     return generator_mock


# @pytest.fixture
# def mock_scene_manager(monkeypatch):
#     scene_manager_mock = MagicMock()
#     monkeypatch.setitem(
#         __import__("sys").modules,
#         "xodex.scenes.manager",
#         MagicMock(SceneManager=MagicMock(return_value=scene_manager_mock)),
#     )
#     return scene_manager_mock


# def test_cprint_colored(monkeypatch):
#     from xodex.core import management

#     monkeypatch.setattr(management, "COLOR_ENABLED", True)

#     class DummyFore:
#         RED = "RED"

#     class DummyStyle:
#         RESET_ALL = ""

#     monkeypatch.setattr(management, "Fore", DummyFore)
#     monkeypatch.setattr(management, "Style", DummyStyle)
#     # Should not raise
#     management.cprint("test", color="red")


# def test_execute_run(monkeypatch, mock_game):
#     util = ManagementUtility(["prog", "run"])
#     util.run_game = MagicMock()
#     util.execute()
#     util.run_game.assert_called_once()


# def test_execute_startgame(monkeypatch):
#     util = ManagementUtility(["prog", "startgame", "--name", "foo"])
#     util.generate = MagicMock()
#     util.execute()
#     util.generate.assert_called_once()


# def test_execute_build(monkeypatch):
#     util = ManagementUtility(["prog", "build", "--name", "foo"])
#     util.build = MagicMock()
#     util.execute()
#     util.build.assert_called_once()


# def test_execute_pause_resume(monkeypatch, mock_game):
#     util = ManagementUtility(["prog", "pause"])
#     util.pause_game = MagicMock()
#     util.execute()
#     util.pause_game.assert_called_once()
#     util = ManagementUtility(["prog", "resume"])
#     util.resume_game = MagicMock()
#     util.execute()
#     util.resume_game.assert_called_once()


# def test_execute_reloadscene(monkeypatch, mock_game):
#     util = ManagementUtility(["prog", "reloadscene"])
#     util.reload_scene = MagicMock()
#     util.execute()
#     util.reload_scene.assert_called_once()


# def test_execute_toggledebug(monkeypatch, mock_game):
#     util = ManagementUtility(["prog", "toggledebug"])
#     util.toggle_debug = MagicMock()
#     util.execute()
#     util.toggle_debug.assert_called_once()


# def test_execute_showfps(monkeypatch, mock_game):
#     util = ManagementUtility(["prog", "showfps"])
#     util.toggle_fps = MagicMock()
#     util.execute()
#     util.toggle_fps.assert_called_once()


# def test_execute_listscenes(monkeypatch, mock_scene_manager):
#     util = ManagementUtility(["prog", "listscenes"])
#     util.list_scenes = MagicMock()
#     util.execute()
#     util.list_scenes.assert_called_once()


# def test_print_help(capsys):
#     util = ManagementUtility(["prog", "help"])
#     util.print_help()
#     out = capsys.readouterr().out
#     assert "Available commands" in out


# if __name__ == "__main__":
#     pytest.main(["-v", "--tb=short", __file__])
