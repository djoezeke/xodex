"""Scenes"""

from xodex.scenes.base_scene import BaseScene
from xodex.scenes.blur_scene import BlurScene
from xodex.scenes.manager import SceneManager, register

__all__ = ("SceneManager", "Scene", "BlurScene", "register")


class Scene(BaseScene):
    """Scene"""
