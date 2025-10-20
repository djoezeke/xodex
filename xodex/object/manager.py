"""Objects Manager

Provides scene-based registration and querying of game objects.
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable

from xodex.core.exceptions import AlreadyRegistered
from xodex.core.exceptions import NotRegistered
from xodex.core.exceptions import ObjectError
from xodex.object.base import Object
from xodex.utils.log import get_xodex_logger
from xodex.utils.singleton import Singleton
from xodex.utils.values import Values

__all__ = ("ObjectsManager", "register")


logger = get_xodex_logger(__name__)


class BaseManager(Singleton):
    """
    Objects registry for game objects.

    Features:
        - Registration and lookup by name, class, or index
        - Stack navigation (push, pop, replace, clear, swap, jump)
        - Hooks for before/after register/unregister
        - Async support for hooks
        - Logging for key actions

    Usage:
        manager = ObjectsManager()
        manager.register(MyObject, "MyObject")
        obj_cls = manager.get_object("MyObject")
        manager.unregister("MyObject")
    """

    def __init__(self):
        self.__object_classes: dict[str, type[Object]] = {}
        self._user_hooks: dict[str, list[Callable]] = {}

    # region Properties

    @property
    def all(self) -> list[type[Object]]:
        """Return a list of all registered object classes."""
        return list(self.__object_classes.values())

    @property
    def count(self) -> int:
        """Return the number of registered object classes."""
        return len(self.__object_classes)

    # endregion

    # region Registration

    def register(self, object_class: type[Object], object_name: str) -> None:
        """
        Register an object class with a given name.

        Raises:
            AlreadyRegistered: If the object is already registered.
            ObjectError: If the class is not a subclass of Object.
        """
        self._run_hook("before_register", object_class, object_name)
        if not issubclass(object_class, Object):
            raise ObjectError(f"{object_class} is not a subclass of Object.")
        if self.is_registered(object_name):
            raise AlreadyRegistered(f"The Object '{object_name}' is already registered.")
        self.__object_classes[object_name] = object_class
        logger.info(f"Registered object '{object_name}'.")
        self._run_hook("after_register", object_class, object_name)

    def unregister(self, object_name: str) -> None:
        """
        Unregister an object class by name.

        Raises:
            NotRegistered: If the object is not registered.
        """
        self._run_hook("before_unregister", object_name)
        if not self.is_registered(object_name):
            raise NotRegistered(f"The Object '{object_name}' is not registered.")
        del self.__object_classes[object_name]
        logger.info(f"Unregistered object '{object_name}'.")
        self._run_hook("after_unregister", object_name)

    def is_registered(self, object_name: str) -> bool:
        """Return True if an object is registered by name."""
        return object_name in self.__object_classes

    def get_object(self, object_name: str) -> type[Object]:
        """
        Get a registered object class by name.

        Raises:
            KeyError: If the object is not registered.
        """
        return self._get_object_(object_name)

    def get_objects(self) -> Values:
        """Get all registered object classes as a Values object."""
        return Values(self.__object_classes)

    def list_registered_object_classes(self) -> list[str]:
        """List all registered object class names."""
        return list(self.__object_classes.keys())

    def clear(self) -> None:
        """Remove all registered object classes."""
        self.__object_classes.clear()
        logger.info("Cleared all registered objects.")

    # endregion

    # region Lookup

    def get_object_by_index(self, index: int) -> type[Object] | None:
        """
        Get an object class by index.

        Args:
            index: Index of the object.

        Returns:
            The object class, or None if out of range.
        """
        keys = list(self.__object_classes.keys())
        if 0 <= index < len(keys):
            return self.__object_classes[keys[index]]
        logger.warning(f"Object index {index} out of range.")
        return None

    def find_object_by_class(self, cls: type[Object]) -> str | None:
        """
        Find the registered name for a given object class.

        Args:
            cls: The object class.

        Returns:
            The registered name, or None if not found.
        """
        for name, obj_cls in self.__object_classes.items():
            if obj_cls is cls:
                return name
        return None

    # endregion

    # region Hooks

    def add_hook(self, event: str, callback: Callable) -> None:
        """
        Add a user callback for an object event.

        Args:
            event: "before_register", "after_register", etc.
            callback: Callable to run.
        """
        self._user_hooks.setdefault(event, []).append(callback)

    def _run_hook(self, event: str, *args, **kwargs) -> None:
        """Run user hooks for a given event."""
        for cb in self._user_hooks.get(event, []):
            try:
                cb(self, *args, **kwargs)
            except Exception as e:
                logger.error(f"Error in user hook '{event}': {e}")

    async def async_run_hook(self, event: str, *args, **kwargs) -> None:
        """Async version of _run_hook."""
        for cb in self._user_hooks.get(event, []):
            try:
                if asyncio.iscoroutinefunction(cb):
                    await cb(self, *args, **kwargs)
                else:
                    cb(self, *args, **kwargs)
            except Exception as e:
                logger.error(f"Error in async user hook '{event}': {e}")

    # endregion

    # region Private

    def _get_object_(self, object_name: str) -> type[Object]:
        _object = self.__object_classes.get(object_name)
        if _object is not None:
            return _object
        raise KeyError(f"{object_name} is not a valid Object")

    # endregion

    def __len__(self) -> int:
        """Return the number of registered object classes."""
        return len(self.__object_classes)

    def __contains__(self, key: str) -> bool:
        """Check if an object is registered by name."""
        return key in self.__object_classes


class ObjectsManager(BaseManager): ...


def register(cls=None, *, name: str = None):
    """
    Decorator for registering objects.

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
