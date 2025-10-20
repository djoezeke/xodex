# from unittest.mock import MagicMock

# import pygame
# import pytest
# from xodex.core.exceptions import AlreadyRegistered
# from xodex.game.sounds import Sounds


# @pytest.fixture(autouse=True)
# def patch_pygame_mixer(monkeypatch):
#     # Patch pygame.mixer and Sound/Channel to avoid real audio
#     monkeypatch.setattr(pygame.mixer, "music", MagicMock())
#     monkeypatch.setattr(pygame.mixer, "pause", MagicMock())
#     monkeypatch.setattr(pygame.mixer, "unpause", MagicMock())
#     monkeypatch.setattr("pygame.mixer.Sound", MagicMock())
#     monkeypatch.setattr("pygame.mixer.Channel", MagicMock())
#     yield


# @pytest.fixture
# def sounds(tmp_path, monkeypatch):
#     # Patch os.listdir to simulate sound files
#     monkeypatch.setattr("os.listdir", lambda d: ["a.wav", "b.ogg", "c.mp3", "notasound.txt"])
#     s = Sounds()
#     s.clear()  # Start with empty registry
#     return s


# def test_register_and_unregister_sound(sounds):
#     fake_sound = MagicMock()
#     sounds.register(fake_sound, "test")
#     assert "test" in sounds.list_sounds()
#     with pytest.raises(AlreadyRegistered):
#         sounds.register(fake_sound, "test")
#     sounds.unregister("test")
#     assert "test" not in sounds.list_sounds()


# def test_isregistered(sounds):
#     fake_sound = MagicMock()
#     sounds.register(fake_sound, "foo")
#     assert sounds.isregistered("foo")
#     sounds.unregister("foo")
#     assert not sounds.isregistered("foo")


# def test_new_channel_and_list_channels(sounds):
#     sounds.new_channel("chan1")
#     sounds.new_channel("chan2")
#     assert set(sounds.list_channels()) == {"chan1", "chan2"}


# def test_set_volume_and_channel_volume(sounds):
#     fake_sound = MagicMock()
#     fake_channel = MagicMock()
#     sounds.register(fake_sound, "voltest")
#     sounds._Sounds__channels["chan"] = fake_channel
#     sounds.set_volume("voltest", 0.5)
#     fake_sound.set_volume.assert_called_with(0.5)
#     sounds.set_channel_volume("chan", 0.7)
#     fake_channel.set_volume.assert_called_with(0.7)


# def test_remove_stopped(sounds):
#     fake_channel = MagicMock()
#     fake_channel.get_busy.return_value = False
#     sounds._Sounds__channels["chan"] = fake_channel
#     sounds.remove_stopped()
#     assert "chan" not in sounds._Sounds__channels


# def test_list_sounds_and_channels(sounds):
#     fake_sound = MagicMock()
#     sounds.register(fake_sound, "s1")
#     sounds.new_channel("c1")
#     assert "s1" in sounds.list_sounds()
#     assert "c1" in sounds.list_channels()


# def test_info(sounds):
#     fake_sound = MagicMock()
#     sounds.register(fake_sound, "s1")
#     sounds.new_channel("c1")
#     info = sounds.info()
#     assert "sounds" in info and "channels" in info
#     assert "s1" in info["sounds"]
#     assert "c1" in info["channels"]


# def test_preload_sounds(monkeypatch):
#     # Patch Sound to avoid actual loading
#     monkeypatch.setattr("pygame.mixer.Sound", MagicMock())
#     s = Sounds()
#     s.clear()
#     monkeypatch.setattr("os.listdir", lambda d: ["a.wav", "b.ogg", "c.mp3", "notasound.txt"])
#     s.preload_sounds(".")
#     assert set(s.list_sounds()) == {"a", "b", "c"}


# pytest.main(["-v", __file__], plugins=[patch_pygame_mixer])
