import json
import pickle

from xodex.core.singleton import Singleton
from xodex.utils.storage import JsonSerializer, JsonDeserializer, BinarySerializer, BinaryDeserializer


class Storage(Singleton, JsonSerializer, JsonDeserializer, BinarySerializer, BinaryDeserializer):
    """
    Persistent storage manager for game data.

    Supports both JSON and binary (pickle) serialization formats.
    Inherit and override `serialize`/`deserialize` and/or `serialize_binary`/`deserialize_binary`
    for custom object state handling.

    Attributes:
        data_path (str): Directory for storing data files.
        filename (str): Name of the file for saving/loading.
    """

    data_path: str = "."
    binary: bool = False

    def load(self) -> None:
        """
        Load data from file (JSON or binary).

        Args:
            binary (bool): If True, load as binary (pickle). Otherwise, load as JSON.
        """
        if not hasattr(self, "filename"):
            self.filename = f"{self.__class__.__name__.lower()}{'.bxox' if self.binary else '.jxox'}"
        try:
            mode = "rb" if self.binary else "r"
            with open(f"{Storage.data_path}/{self.filename}", mode) as f:
                if self.binary:
                    self.deserialize_binary(f.read())
                else:
                    self.deserialize(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError, pickle.UnpicklingError):
            self.save()

    def save(self) -> None:
        """
        Save data to file (JSON or binary).

        Args:
            binary (bool): If True, save as binary (pickle). Otherwise, save as JSON.
        """
        if not hasattr(self, "filename"):
            self.filename = f"{self.__class__.__name__.lower()}{'.bxox' if self.binary else '.jxox'}"
        try:
            mode = "wb" if self.binary else "w"
            with open(f"{Storage.data_path}/{self.filename}", mode) as f:
                if self.binary:
                    f.write(self.serialize_binary())
                else:
                    json.dump(self.serialize(), f, indent=2)
        except FileNotFoundError:
            pass

    def event_handler(self, event):
        """
        Handle events related to storage (stub for extension).

        Args:
            event: Event object.
        """
