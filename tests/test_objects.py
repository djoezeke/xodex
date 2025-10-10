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
    l = DummyLogical()
    d = DummyDrawable()
    e = DummyEventful()
    objs.append(l)
    objs.append(d)
    objs.append(e)
    assert l in objs and d in objs and e in objs

    # Should raise ValueError for wrong type
    with pytest.raises(ValueError):
        objs.append(object())


def test_objects_extend_and_insert():
    objs = Objects()
    l = DummyLogical()
    d = DummyDrawable()
    e = DummyEventful()
    objs.extend([l, d])
    assert l in objs and d in objs
    objs.insert(1, e)
    assert objs[1] is e


def test_update_object_calls_logical():
    objs = Objects()
    l = DummyLogical()
    d = DummyDrawable()
    objs.append(l)
    objs.append(d)
    objs.update_object(0.1)
    assert l.updated
    # Drawable should not be updated
    assert not hasattr(d, "updated") or not d.updated


def test_draw_object_calls_drawable():
    objs = Objects()
    l = DummyLogical()
    d = DummyDrawable()
    objs.append(l)
    objs.append(d)
    surf = pygame.Surface((10, 10))
    objs.draw_object(surf)
    assert d.drawn
    # Logical should not be drawn
    assert not hasattr(l, "drawn") or not l.drawn


def test_handle_object_calls_eventful():
    objs = Objects()
    e = DummyEventful()
    objs.append(e)
    event = pygame.event.Event(pygame.USEREVENT)
    objs.handle_object(event)
    assert e.handled


def test_objects_iadd():
    objs = Objects()
    l = DummyLogical()
    d = DummyDrawable()
    objs += [l, d]
    assert l in objs and d in objs


def test_objects_append_class_instantiates():
    objs = Objects()
    objs.append(DummyLogical)
    assert isinstance(objs[0], DummyLogical)


if __name__ == "__main__":
    pytest.main(["-v", "--tb=short", __file__])
