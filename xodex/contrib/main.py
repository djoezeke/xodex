"""Main Game Scene"""

from typing import Generator

from xodex.scenes.base_scene import BaseScene

# from xodex.core.localization import localize


class XodexMainScene(BaseScene):
    """XodexMainScene"""

    def __init__(self):
        super().__init__()

    # region Private

    def _generate_objects_(self) -> Generator:
        text = self.object.get_object(object_name="XodexText")

        yield text("Hello", (100, 100))
        yield text("Hello", (100, 150))
        yield text("Hello", (100, 200))

    # endregion

    # region Public

    # endregion


class XodexUIScene(BaseScene):
    """XodexUIScene

    Demonstrates PygameUI widgets in a Xodex scene, including labels, buttons, and event handling.
    """

    def __init__(self):
        super().__init__()

    def _generate_objects_(self):
        # Get Xodex-wrapped PygameUI widgets
        label_cls = self.get_object(object_name="UILABEL")
        button_cls = self.get_object(object_name="UIBTN")
        entry_cls = self.get_object(object_name="UIENTRY")
        # Fallbacks for attribute access
        label_cls2 = getattr(self.object, "UILABEL", None)
        button_cls2 = getattr(self.object, "UIBTN", None)
        entry_cls2 = getattr(self.object, "UIENTRY", None)

        # Demo label
        label1 = label_cls(master=self._screen, text="Welcome to Xodex UI Demo")
        label1.place(x=100, y=50)

        # Entry widget for user input
        entry = None
        if entry_cls:
            entry = entry_cls(master=self._screen, width=200, text="Type here...")
            entry.place(x=100, y=100)
            yield entry

        # Dynamic label to show button clicks
        status_label = label_cls(master=self._screen, text="Button not clicked yet")
        status_label.place(x=100, y=150)

        # Button with event binding
        def on_button_click(*args, **kwargs):
            status_label.configure(text="Button clicked!")

        button = button_cls(master=self._screen, text="Click Me")
        # Try to bind the click event (if available)
        if hasattr(button, "bind"):
            # PygameUI usually uses pygame.MOUSEBUTTONDOWN or a custom event
            # import pygame
            # button.bind(pygame.MOUSEBUTTONDOWN, on_button_click)
            pass
        else:
            # Fallback: override handle_event
            orig_handle = getattr(button, "handle_event", None)
            def handle_event(event, *a, **kw):
                import pygame
                if event.type == pygame.MOUSEBUTTONDOWN:
                    on_button_click()
                if orig_handle:
                    orig_handle(event, *a, **kw)
            button.handle_event = handle_event

        button.place(x=100, y=200)

        # Add a second label and button for variety
        label2 = label_cls2(master=self._screen, text="Another Label") if label_cls2 else None
        if label2:
            label2.place(x=350, y=50)
            yield label2

        button2 = button_cls2(master=self._screen, text="Another Button") if button_cls2 else None
        if button2:
            button2.place(x=350, y=100)
            yield button2

        # Yield all widgets to the scene
        yield label1
        yield status_label
        yield button

        # Optionally, yield more widgets for demonstration
        if entry:
            yield entry

        # Add a text object for legacy Xodex text
        text = self.get_object(object_name="XodexText")
        if text:
            yield text("Legacy XodexText object", (10, 300))
