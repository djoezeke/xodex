"""Main Game Scene"""

from __future__ import annotations

from collections.abc import Generator

from xodex.scene.base import BaseScene

# from xodex.core.localization import localize


class XodexMainScene(BaseScene):
    """XodexMainScene"""

    def __init__(self):
        super().__init__()

    # region Private

    def _generate_objects_(self) -> Generator:
        text = self.get_object(object_name="XodexText")

        yield text("Hello", (100, 100))
        yield text("Hello", (100, 150))
        yield text("Hello", (100, 200))

    # endregion

    # region Public

    # endregion
