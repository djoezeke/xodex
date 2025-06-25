import os
from typing import Optional
from importlib import import_module

import pygame
from pygame.mixer import Sound, Channel

from xodex.utils.values import Values
from xodex.core.singleton import Singleton
from xodex.core.exceptions import NotRegistered, AlreadyRegistered, ObjectError


class Sounds(Singleton):
    """
    Singleton class for managing sound effects and channels using pygame.mixer.
    Provides registration, playback, volume, and introspection utilities.
    """

    _channels: dict[str, Channel] = {}
    _music: str = None
    _channel_count: int = 0

    def __init__(self, folder: str = "."):
        self.sound_folder = None
        try:
            xodex_settings = os.getenv("XODEX_SETTINGS_MODULE")
            self.setting = import_module(xodex_settings)
            self.sound_folder = self.setting.SOUND_DIR
        except Exception:
            pass
        self.sound_folder = self.sound_folder or folder
        self.__sounds: dict[str, Sound] = {}
        self.load_sounds(self.sound_folder)

    def __len__(self) -> int:
        return len(self.__sounds)

    def __contains__(self, key: str) -> bool:
        return key in self.__sounds

    def __repr__(self):
        """Return a string representation of Sounds."""
        return f"{self.__class__.__name__}()"

    def __str__(self):
        """Return a string representation of Sounds."""
        return f"<{self.__class__.__name__} in {self.sound_folder}>"

    # region Music

    @classmethod
    def play_music(cls, loops: int = -1, start: float = 0, fade_ms: int = 0):
        """Play background music."""
        try:
            pygame.mixer.music.load(Sounds._music)
            pygame.mixer.music.play(loops, start, fade_ms)
        except Exception:
            pass

    @classmethod
    def set_music(cls, filename: str):
        """Load background music."""
        cls._music = filename

    @classmethod
    def stop_music(cls):
        """Stop playing background music."""
        pygame.mixer.music.stop()

    @classmethod
    def set_music_volume(cls, volume: float):
        """Pause background music."""
        pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))

    @classmethod
    def pause_music(cls):
        """Pause background music."""
        pygame.mixer.music.pause()

    @classmethod
    def unpause_music(cls):
        """Unpause background music."""
        pygame.mixer.music.unpause()

    # endregion

    # region Sound/Channel
    def play(
        self, sound: str, channel: str = "", loops: int = 0, maxtime: int = 0, fade_ms: int = 0
    ) -> Optional[Channel]:
        """Play a sound by name, optionally on a named channel."""
        try:
            if channel == "":
                ch = self.__sounds[sound].play(loops, maxtime, fade_ms)
            else:
                ch = Sounds._channels[channel].play(self.__sounds[sound], loops, maxtime, fade_ms)
            return ch
        except KeyError:
            print(f"Sound or channel '{sound}'/'{channel}' not found.")

    def stop(self, sound: str):
        """Play a sound by name, optionally on a named channel."""
        try:
            self.__sounds[sound].stop()
        except KeyError:
            print(f"Sound '{sound}' not found.")
        else:
            try:
                Sounds._channels[sound].stop()
            except KeyError:
                print(f"Channel '{sound}' not found.")

    def set_volume(self, sound, volume: float):
        """Pause background music."""
        try:
            self.__sounds[sound].set_volume(max(0.0, min(1.0, volume)))
        except KeyError:
            print(f"Sound '{sound}' not found.")
        else:
            try:
                Sounds._channels[sound].set_volume(max(0.0, min(1.0, volume)))
            except KeyError:
                print(f"Channel '{sound}' not found.")

    @classmethod
    def pause(cls, channel: str) -> None:
        """Pause playback on a channel."""
        try:
            cls._channels[channel].pause()
        except KeyError:
            pass

    @classmethod
    def unpause(cls, channel: str) -> None:
        """Unpause playback on a channel."""
        try:
            cls._channels[channel].unpause()
        except KeyError:
            pass

    # endregion Sound

    def pause_all(self):
        """Pause all channels."""
        pygame.mixer.pause()

    def unpause_all(self):
        """Unpause all channels."""
        pygame.mixer.unpause()

    @classmethod
    def channels(cls) -> Values:
        """Return all registered channels."""
        return Values(cls._channels)

    def sounds(self) -> Values:
        """Return all registered sounds."""
        return Values(self.__sounds)

    def play_if_not_busy(
        self, channel: str, sound: str, loops: int = 0, maxtime: int = 0, fade_ms: int = 0
    ) -> Optional[Channel]:
        """
        Play a sound on a channel only if the channel is not busy.
        """
        if not self.is_busy(channel):
            return self.play(sound, channel, loops, maxtime, fade_ms)
        return None

    def reset_play(self, channel: str, sound: str) -> Optional[Channel]:
        """
        Play a sound on a channel only if it's not already playing that sound.
        """
        try:
            main_sound = self.__sounds[sound]
        except KeyError:
            return None
        if self.get_sound(channel) is main_sound:
            return None
        return self.play(sound, channel)

    @classmethod
    def get_sound(cls, channel: str) -> Optional[Sound]:
        """
        Get the currently playing Sound object on a channel.
        """
        try:
            return cls._channels[channel].get_sound()
        except KeyError:
            return None

    @classmethod
    def is_busy(cls, channel: str) -> bool:
        """
        Check if a channel is currently playing any sound.
        """
        try:
            return cls._channels[channel].get_busy()
        except KeyError:
            return False

    def register(self, sound: Sound, sound_name: str):
        """
        Register a Sound object with a name.
        """
        if not isinstance(sound, Sound):
            raise ObjectError(f"The Sound {sound_name} is not of type Sound.")
        if self.isregistered(sound_name):
            raise AlreadyRegistered(f"The Sound {sound_name} is already registered.")
        self.__sounds[sound_name] = sound

    def unregister(self, sound_name: str) -> None:
        """
        Unregister a Sound by name.
        """
        if not self.isregistered(sound_name):
            raise NotRegistered(f"The Sound {sound_name} is not registered")
        del self.__sounds[sound_name]

    def isregistered(self, sound_name: str) -> bool:
        """
        Return True if a Sound is registered.
        """
        return sound_name in self.__sounds

    @classmethod
    def new_channel(cls, channel_name: str):
        """Create and register a new Channel with a name."""
        if not channel_name:
            return
        channel = Channel(cls._channel_count)
        cls._channels[channel_name] = channel
        cls._channel_count += 1

    @classmethod
    def remove_stopped(cls):
        """Remove channels that are not playing any sound."""
        to_remove = [name for name, ch in cls._channels.items() if not ch.get_busy()]
        for name in to_remove:
            del cls._channels[name]

    def load(self, filename: str, sound_name: str = ""):
        """Load Sound music."""
        if filename in os.listdir(self.sound_folder):
            try:
                sound = Sound(os.path.join(self.sound_folder, filename))
                if sound_name == "":
                    self.register(sound, os.path.splitext(filename)[0])
                else:
                    self.register(sound, sound_name)
            except Exception as e:
                print(f"Failed to load sound {filename}: {e}")

    def load_sounds(self, directory: str, extensions: tuple = (".wav", ".ogg", ".mp3")):
        """Load all sounds from a directory with given extensions."""
        try:
            for fname in os.listdir(directory):
                if fname.endswith(extensions):
                    self.load(fname)
        except Exception:
            print(f"Cannot find the path: '{directory}'")

    def list_sounds(self):
        """List all registered sound names."""
        return list(self.__sounds.keys())

    @classmethod
    def list_channels(cls):
        """List all registered channel names."""
        return list(cls._channels.keys())

    def clear(self):
        """
        Clear all registered sounds and channels.
        """
        self.__sounds.clear()

    def info(self) -> dict:
        """
        Get a summary of the current sound system state.
        """
        return {
            "sounds": self.list_sounds(),
            "channels": Sounds.list_channels(),
        }
