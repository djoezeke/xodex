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
    """XodexUIScene"""

    def __init__(self):
        super().__init__()

    def _generate_objects_(self):
        text = self.get_object(object_name="XodexText")
        label = self.get_object(object_name="UILABEL")
        btn = self.get_object(object_name="UIBTN")
        labell = self.object.UILABEL
        btnn = self.object.UIBTN

        label1 = label(master=self._screen, text="My Label")
        label1.place(x=100, y=200)

        label2 = labell(master=self._screen, text="My Label")
        label2.place(x=100, y=400)

        btn2 = btnn(master=self._screen, text="Click")
        btn2.place(x=400, y=400)

        btn1 = btn(master=self._screen, text="Click Me")
        btn1.place(x=100, y=300)

        yield label1
        yield btn1
        yield label2
        yield btn2

        yield text("Hello", (10, 100))
