"""Objects Manager

Provides scene-based registration and querying of game objects.
"""

from typing import Union
from xodex.utils.values import Values
from xodex.objects.image import Image
from xodex.objects.animator import Animator
from xodex.core.singleton import Singleton
from xodex.contrib.basicobjects import XodexText
from xodex.objects.objects import Object, DrawableObject, EventfulObject, LogicalObject
from xodex.core.exceptions import NotRegistered, AlreadyRegistered, ObjectError


try:
    import pygameui

    HAS_PYGAMEUI = True
except ImportError:
    HAS_PYGAMEUI = False

if HAS_PYGAMEUI:
    from xodex.contrib.pygameui import (
        UIBUTTON,
        UICHECKBUTTON,
        UICOMBOBOX,
        UIENTRY,
        UIFLOODGAUGE,
        UIFRAME,
        UILABEL,
        UILISTBOX,
        UIMENUBUTTON,
        UIMETER,
        UIPROGRESSBAR,
        UIRADIOBUTTON,
        UISCALE,
        UISEPERATOR,
        UISIZEGRIP,
        UISPINBOX,
        UITEXTBOX,
        UITREEVIEW,
    )

__all__ = ("ObjectsManager", "register")


class ObjectsManager(Singleton):
    """
    Objects registry for game objects.
    """

    def __init__(self):
        self.__object_classes: dict[str, Object] = {}

        # Register default objects
        self.register(XodexText, "XodexText")
        self.register(Image, "Image")  # prom
        self.register(Animator, "Animator")  # flappy

        if HAS_PYGAMEUI:
            self.register(UIFRAME, "UIFRAME")
            self.register(UILABEL, "UILABEL")
            self.register(UIENTRY, "UIENTRY")
            self.register(UIMETER, "UIMETER")
            self.register(UISCALE, "UISCALE")
            self.register(UIBUTTON, "UIBUTTON")
            self.register(UITEXTBOX, "UITEXTBOX")
            self.register(UISPINBOX, "UISPINBOX")
            self.register(UILISTBOX, "UILISTBOX")
            self.register(UISIZEGRIP, "UISIZEGRIP")
            self.register(UITREEVIEW, "UITREEVIEW")
            self.register(UICOMBOBOX, "UICOMBOBOX")
            self.register(UISEPERATOR, "UISEPERATOR")
            self.register(UIMENUBUTTON, "UIMENUBUTTON")
            self.register(UIFLOODGAUGE, "UIFLOODGAUGE")
            self.register(UICHECKBUTTON, "UICHECKBUTTON")
            self.register(UIRADIOBUTTON, "UIRADIOBUTTON")
            self.register(UIPROGRESSBAR, "UIPROGRESSBAR")

    def __len__(self) -> int:
        return len(self.__object_classes)

    def __contains__(self, key: str) -> bool:
        return key in self.__object_classes.keys()

    def get_object(self, object_name: str) -> Union[DrawableObject, EventfulObject, LogicalObject]:
        """Get an object."""
        return self._get_object_(object_name)

    def get_objects(self) -> Values:
        """Get an object."""
        return Values(self.__object_classes)

    def clear(self):
        """Remove all objects."""
        self.__object_classes.clear()

    def register(self, object_class: Object, object_name: str):
        """register a Object Class"""

        if issubclass(object_class, Object):
            if self.isregistered(object_class):
                msg = "The Object %s is already registered "
                raise AlreadyRegistered(msg)

            self.__object_classes[object_name] = object_class
        else:
            msg = "The Object %s is not of type Object."
            raise ObjectError(msg)

    def unregister(self, object_name: str) -> None:
        """unregister a Object Class"""
        if not self.isregistered(object_name):
            raise NotRegistered(f"The Object {object_name} is not registered")
        del self.__object_classes[object_name]

    def isregistered(self, object_name: str) -> bool:
        """Return true if Object is registered"""
        return object_name in self.__object_classes

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
