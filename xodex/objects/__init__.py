"""Objects

Provides:
- Objects: A type-safe, ordered container for game objects.
- ObjectsManager: Scene-based registry for all objects.
- Base object types: DrawableObject, EventfulObject, LogicalObject.
"""

from typing import Iterable

from pygame import Surface
from pygame.event import Event

from xodex.objects.manager import ObjectsManager, register
from xodex.objects.objects import Object, DrawableObject, EventfulObject, LogicalObject

__all__ = (
    "DrawableObject",
    "EventfulObject",
    "LogicalObject",
    "ObjectsManager",
    "Objects",
    "Object",
    "register",
)


class Objects(list):
    """A type-safe, ordered container for game objects."""

    _allowed_types_ = (LogicalObject, DrawableObject, EventfulObject)

    def __init__(self):
        list.__init__(self)

    # region Private
    def _check_type_(self, item):
        if not isinstance(item, self._allowed_types_):
            raise ValueError(
                f"Object type: {type(item)}/{item} is not in {self._allowed_types_}"
            )

    def __iadd__(self, other):
        for item in other:
            self._check_type_(item)
        return super().__iadd__(other)

    # endregion

    # region Public

    def append(self, item) -> None:
        """Append an object, enforcing allowed types or instantiating if class."""
        if isinstance(item, type) and issubclass(item, self._allowed_types_):
            item = item()
        self._check_type_(item)
        super().append(item)

    def insert(self, index, item) -> None:
        """Insert an object at a given index, enforcing allowed types or instantiating if class."""
        if isinstance(item, type) and issubclass(item, self._allowed_types_):
            item = item()
        self._check_type_(item)
        super().insert(index, item)

    def extend(self, iterable: Iterable) -> None:
        """Extend with an iterable, enforcing allowed types or instantiating if class."""
        items = []
        for item in iterable:
            if isinstance(item, type) and issubclass(item, self._allowed_types_):
                item = item()
            self._check_type_(item)
            items.append(item)
        super().extend(items)

    def update(self, delta: float = 0.0) -> None:
        """Update all LogicalObjects."""
        filtered: Iterable[LogicalObject] = filter(
            lambda x: isinstance(x, LogicalObject), self
        )
        for obj in filtered:
            obj.update(delta)

    def draw(self, screen: Surface) -> None:
        """Draw all DrawableObjects, sorted by z_index if present."""
        filtered: Iterable[DrawableObject] = filter(
            lambda x: isinstance(x, DrawableObject), self
        )
        sorted_objs = sorted(filtered, key=lambda obj: getattr(obj, "z_index", 0))
        for obj in sorted_objs:
            obj.draw(screen)

    def handle(self, event: Event) -> None:
        """Dispatch event to all EventfulObjects."""
        filtered: Iterable[EventfulObject] = filter(
            lambda x: isinstance(x, EventfulObject), self
        )
        for obj in filtered:
            obj.handle(event)

    # endregion
