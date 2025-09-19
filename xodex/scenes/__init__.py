"""Scenes"""

from xodex.scenes.base_scene import BaseScene
from xodex.scenes.blur_scene import BlurScene
from xodex.scenes.blur_scene import BoxBlurScene
from xodex.scenes.blur_scene import GaussianBlurScene
from xodex.scenes.blur_scene import MaskedBlurScene
from xodex.scenes.blur_scene import MotionBlurScene
from xodex.scenes.manager import register
from xodex.scenes.manager import SceneManager

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
