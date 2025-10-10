"""Scenes"""

from xodex.scene.base import BaseScene
from xodex.scene.blur import BlurScene
from xodex.scene.blur import BoxBlurScene
from xodex.scene.blur import GaussianBlurScene
from xodex.scene.blur import MaskedBlurScene
from xodex.scene.blur import MotionBlurScene
from xodex.scene.manager import register
from xodex.scene.manager import SceneManager

__all__ = (
    "Scene",
    "register",
    "BlurScene",
    "BlurScene",
    "SceneManager",
    "BoxBlurScene",
    "GaussianBlurScene",
    "MaskedBlurScene",
    "MotionBlurScene",
)


class Scene(BaseScene):
    """Scene"""
