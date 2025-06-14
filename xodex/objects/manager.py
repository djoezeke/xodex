"""Objects Manager

Provides scene-based registration and querying of game objects.
"""

from typing import Any

from xodex.core.singleton import Singleton
from xodex.contrib.text import XodexText

__all__ = ("ObjectsManager", "register")


class ObjectsManager(Singleton):
    """
    Objects registry for game objects.
    """

    def __init__(self):
        self.__object_classes: dict[str, Any] = {}

        # Register default objects
        self.register(XodexText, "XodexText")

    def __len__(self) -> int:
        return len(self.__object_classes)

    def __getattr__(self, object_name: str) -> Any:
        """Get object."""
        return self.__object_classes.get(object_name, None)

    def __contains__(self, key: str) -> bool:
        return key in self.__object_classes.keys()

    def get_object(self, object_name: str) -> Any:
        """Get an object."""
        return self._get_object_(object_name)

    def clear(self):
        """Remove all objects."""
        self.__object_classes.clear()

    def register(self, object_class: Any, object_name: str):
        """register a Object Class"""
        self.__object_classes[object_name] = object_class

    # region Private

    def _get_object_(self, object_name: str) -> None:
        _object = self.__object_classes.get(object_name)
        if _object is not None:
            return _object
        raise KeyError(f"{object_name} is not a valid Object")

    # endregion


def register(cls=None, *, name: str = None):
    """
    Decorator for registering objects (future extension).
    Usage:
        @register
        class Button(LogicalObject, DrawableObject, EventfulObject):...
    or:
        @register(name="text")
        class Text(DrawableObject, EventfulObject):...
    """

    def decorator(object_cls):
        object_name = name or object_cls.__name__
        ObjectsManager().register(object_cls, object_name)
        return object_cls

    if cls is None:
        return decorator
    return decorator(cls)
