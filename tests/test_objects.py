import pygame
import pytest

from xodex.object import DrawableObject
from xodex.object import EventfulObject
from xodex.object import LogicalObject
from xodex.object import Objects

# --- Dummy implementations for testing ---


class DummyLogical(LogicalObject):
    def __init__(self):
        self.updated = False

    def perform_update(self, deltatime, *a, **k):
        self.updated = True


class DummyDrawable(DrawableObject):
    def __init__(self):
        self.drawn = False

    def perform_draw(self, surface, *a, **k):
        self.drawn = True


class DummyEventful(EventfulObject):
    def __init__(self):
        self.handled = False

    def handle_event(self, event, *a, **k):
        self.handled = True


def test_objects_append_and_type_check():
    objs = Objects()
    logical = DummyLogical()
    drawable = DummyDrawable()
    eventful = DummyEventful()
    objs.append(logical)
    objs.append(drawable)
    objs.append(eventful)
    assert logical in objs and drawable in objs and eventful in objs

    # Should raise ValueError for wrong type
    with pytest.raises(ValueError):
        objs.append(object())


def test_objects_extend_and_insert():
    objs = Objects()
    logical = DummyLogical()
    drawable = DummyDrawable()
    eventful = DummyEventful()
    objs.extend([logical, drawable])
    assert logical in objs and drawable in objs
    objs.insert(1, eventful)
    assert objs[1] is eventful


def test_update_object_calls_logical():
    objs = Objects()
    logical = DummyLogical()
    drawable = DummyDrawable()
    objs.append(logical)
    objs.append(drawable)
    objs.update_object(0.1)
    assert logical.updated
    # Drawable should not be updated
    assert not hasattr(drawable, "updated") or not drawable.updated


def test_draw_object_calls_drawable():
    objs = Objects()
    logical = DummyLogical()
    drawable = DummyDrawable()
    objs.append(logical)
    objs.append(drawable)
    surf = pygame.Surface((10, 10))
    objs.draw_object(surf)
    assert drawable.drawn
    # Logical should not be drawn
    assert not hasattr(logical, "drawn") or not logical.drawn


def test_handle_object_calls_eventful():
    objs = Objects()
    eventful = DummyEventful()
    objs.append(eventful)
    event = pygame.event.Event(pygame.USEREVENT)
    objs.handle_object(event)
    assert eventful.handled


def test_objects_iadd():
    objs = Objects()
    logical = DummyLogical()
    drawable = DummyDrawable()
    objs += [logical, drawable]
    assert logical in objs and drawable in objs


def test_objects_append_class_instantiates():
    objs = Objects()
    objs.append(DummyLogical)
    assert isinstance(objs[0], DummyLogical)


if __name__ == "__main__":
    pytest.main(["-v", "--tb=short", __file__])
