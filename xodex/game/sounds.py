from typing import Optional, Callable, Any
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

    def __init__(self):
        self.__sounds: dict[str, Sound] = {}
        self.__channels: dict[str, Channel] = {}
        self._channel_count = 0
        self._sound_callbacks: dict[str, list[Callable[[str], Any]]] = {}

    def __len__(self) -> int:
        return len(self.__sounds)

    def __contains__(self, key: str) -> bool:
        return key in self.__sounds

    def play_music(self, music_file: str, loops: int = -1, start: float = 0.0, fade_ms: int = 0) -> bool:
        """
        Play background music from a file.
        """
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(loops=loops, start=start, fade_ms=fade_ms)
            return True
        except Exception as e:
            print(f"Error playing music: {e}")
            return False

    def stop_music(self):
        """Stop playing background music."""
        pygame.mixer.music.stop()

    def pause_music(self):
        """Pause background music."""
        pygame.mixer.music.pause()

    def unpause_music(self):
        """Unpause background music."""
        pygame.mixer.music.unpause()

    def pause_all(self):
        """Pause all channels."""
        pygame.mixer.pause()

    def unpause_all(self):
        """Unpause all channels."""
        pygame.mixer.unpause()

    def channels(self) -> Values:
        """Return all registered channels."""
        return Values(self.__channels)

    def sounds(self) -> Values:
        """Return all registered sounds."""
        return Values(self.__sounds)

    def play(self, sound: str, channel: str = "", loops: int = 0, maxtime: int = 0, fade_ms: int = 0) -> Optional[Channel]:
        """
        Play a sound by name, optionally on a named channel.
        """
        try:
            if channel == "":
                ch = self.__sounds[sound].play(loops, maxtime, fade_ms)
            else:
                ch = self.__channels[channel].play(self.__sounds[sound], loops, maxtime, fade_ms)
            self._trigger_callbacks(sound)
            return ch
        except KeyError:
            print(f"Sound or channel '{sound}'/'{channel}' not found.")
            return None

    def play_if_not_busy(self, channel: str, sound: str, loops: int = 0, maxtime: int = 0, fade_ms: int = 0) -> Optional[Channel]:
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

    def get_sound(self, channel: str) -> Optional[Sound]:
        """
        Get the currently playing Sound object on a channel.
        """
        try:
            return self.__channels[channel].get_sound()
        except KeyError:
            return None

    def is_busy(self, channel: str) -> bool:
        """
        Check if a channel is currently playing any sound.
        """
        try:
            return self.__channels[channel].get_busy()
        except KeyError:
            return False

    def stop(self, channel: str) -> None:
        """
        Stop playback on a channel.
        """
        try:
            self.__channels[channel].stop()
        except KeyError:
            pass

    def pause(self, channel: str) -> None:
        """
        Pause playback on a channel.
        """
        try:
            self.__channels[channel].pause()
        except KeyError:
            pass

    def unpause(self, channel: str) -> None:
        """
        Unpause playback on a channel.
        """
        try:
            self.__channels[channel].unpause()
        except KeyError:
            pass

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

    def new_channel(self, channel_name: str):
        """
        Create and register a new Channel with a name.
        """
        if not channel_name:
            return
        channel = Channel(self._channel_count)
        self.__channels[channel_name] = channel
        self._channel_count += 1

    def set_volume(self, sound_name: str, volume: float):
        """
        Set volume for a specific sound (0.0 to 1.0).
        """
        if sound_name in self.__sounds:
            self.__sounds[sound_name].set_volume(volume)

    def set_channel_volume(self, channel_name: str, volume: float):
        """
        Set volume for a specific channel (0.0 to 1.0).
        """
        if channel_name in self.__channels:
            self.__channels[channel_name].set_volume(volume)

    def remove_stopped(self):
        """
        Remove channels that are not playing any sound.
        """
        to_remove = [name for name, ch in self.__channels.items() if not ch.get_busy()]
        for name in to_remove:
            del self.__channels[name]

    def list_sounds(self):
        """
        List all registered sound names.
        """
        return list(self.__sounds.keys())

    def list_channels(self):
        """
        List all registered channel names.
        """
        return list(self.__channels.keys())

    def preload_sounds(self, directory: str, extensions: tuple = ('.wav', '.ogg', '.mp3')):
        """
        Preload all sounds from a directory with given extensions.
        """
        import os
        for fname in os.listdir(directory):
            if fname.endswith(extensions):
                try:
                    sound = Sound(os.path.join(directory, fname))
                    self.register(sound, os.path.splitext(fname)[0])
                except Exception as e:
                    print(f"Failed to load sound {fname}: {e}")

    def clear(self):
        """
        Clear all registered sounds and channels.
        """
        self.__sounds.clear()
        self.__channels.clear()
        self._channel_count = 0

    def on_play(self, sound_name: str, callback: Callable[[str], Any]):
        """
        Register a callback to be called when a sound is played.
        """
        if sound_name not in self._sound_callbacks:
            self._sound_callbacks[sound_name] = []
        self._sound_callbacks[sound_name].append(callback)

    def _trigger_callbacks(self, sound_name: str):
        """
        Internal: trigger callbacks for a sound.
        """
        for cb in self._sound_callbacks.get(sound_name, []):
            try:
                cb(sound_name)
            except Exception as e:
                print(f"Callback error for sound '{sound_name}': {e}")

    def info(self) -> dict:
        """
        Get a summary of the current sound system state.
        """
        return {
            "sounds": self.list_sounds(),
            "channels": self.list_channels(),
            "channel_count": self._channel_count,
        }
