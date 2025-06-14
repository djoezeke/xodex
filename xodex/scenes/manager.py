from pygame import Surface

from xodex.core.singleton import Singleton
from xodex.scenes.base_scene import BaseScene
from xodex.contrib.main import XodexMainScene

__all__ = ("SceneManager", "register")


class SceneManager(Singleton):
    """Scene Manager with stack navigation, transitions, and scene lookup."""

    def __init__(self):

        self.__scene_classes: dict[str, BaseScene] = {}

        # for Rendering scenes
        self.__scenes: list[BaseScene] = []
        self._current_index: int = 0

        # Register default scenes
        self.register(XodexMainScene, "XodexMainScene")

    def __getattr__(self, object_name: str) -> BaseScene:
        return self.__scene_classes.get(object_name, None)

    def __contains__(self, key: str) -> bool:
        return key in self.__scene_classes.keys()

    def __len__(self) -> int:
        return len(self.__scenes)

    @property
    def current(self) -> BaseScene:
        """Current scene."""
        try:
            return self.__scenes[self._current_index]
        except IndexError:
            print("List of scenes is empty")

    def get_scene(self, scene_name: str) -> BaseScene:
        """Get a registered scene class by name."""
        return self._get_scene_(scene_name)

    def clear(self):
        """Remove all scenes."""
        self.__scenes.clear()
        self.__scene_classes.clear()

    def on_exit_scene(self) -> None:
        """Call on_exit on current scene."""
        if self.__scenes:
            self.current.on_exit()

    def on_last_exit_scene(self) -> None:
        """Call on_last_exit on current scene."""
        if self.__scenes:
            self.current.on_last_exit()

    def process_update(self) -> None:
        """Update current scene."""
        self.current.update()

    def process_event(self, event) -> None:
        """Send event to current scene."""
        self.current.handle(event)

    def process_draw(self) -> Surface:
        """Draw current scene."""
        return self.current.draw()

    def append(self, scene: BaseScene) -> None:
        """Push a new scene onto the stack."""
        self.on_exit_scene()
        scene.setup()
        scene.on_first_enter()
        self.__scenes.append(scene)

    def pop(self) -> BaseScene:
        """Pop the current scene and return it."""
        self.on_last_exit_scene()
        pop_scene = self.__scenes.pop()
        if self.__scenes:
            self.current.on_enter()
        return pop_scene

    def play(self, name: str) -> None:
        """Play a Scene."""
        scene = self._get_scene_(name)
        scene().setup()
        scene().on_first_enter()
        return scene()

    def reset(self, scene: BaseScene) -> None:
        """Replace all scenes with a new one."""
        for s in self.__scenes:
            s.on_last_exit()
        scene.setup()
        scene.on_first_enter()
        self.__scenes = [scene]

    def transition_to(
        self,
        new_scene: BaseScene,
        transition_type: str = "fade",
        duration: float = 1.0,
        name: str = None,
    ):
        """Transition to a new scene with an effect."""
        if transition_type == "fade":
            self._fade_transition(new_scene, duration, name)
        else:
            self.append(new_scene, name=name)

    def _fade_transition(self, new_scene: BaseScene, duration: float, name: str = None):
        import pygame

        screen = pygame.display.get_surface()
        clock = pygame.time.Clock()
        alpha_surface = pygame.Surface(screen.get_size())
        alpha_surface.fill((0, 0, 0))
        for alpha in range(0, 255, max(1, int(255 / (duration * 60)))):
            self.process_draw()
            alpha_surface.set_alpha(alpha)
            screen.blit(alpha_surface, (0, 0))
            pygame.display.flip()
            clock.tick(60)
        self.append(new_scene, name=name)

    def list_scenes(self) -> list[str]:
        """List all named scenes."""
        return list(self.__scene_classes.keys())

    def reload_current(self):
        """Reload the current scene (calls setup and on_first_enter again)."""
        if self.__scenes:
            scene = self.current
            scene.on_last_exit()
            scene.setup()
            scene.on_first_enter()

    def list_registered_scene_classes(self) -> list[str]:
        """List all registered scene class names."""
        return list(self.__scene_classes.keys())

    def register(self, scene_class: BaseScene, scene_name: str):
        """register a Scene Class"""
        self.__scene_classes[scene_name] = scene_class

    # region Private

    def _get_scene_(self, scene_name: str) -> BaseScene:
        """Get a registered scene class by name."""
        scene = self.__scene_classes.get(scene_name)
        if scene is not None:
            return scene
        raise KeyError(f"{scene_name} is not a valid Scene")

    # endregion


def register(cls, *, name: str = None):
    """
    Decorator for registering scene classes with the SceneManager.
    Usage:
        @register
        class MyScene(BaseScene): ...
    or:
        @register(name="custom_name")
        class MyScene(BaseScene): ...
    or:
        @register(BaseScene,name="custom_name")
    """

    def decorator(scene_cls):
        scene_name = name or scene_cls.__name__
        SceneManager().register(scene_cls, scene_name)
        return scene_cls

    if cls is None:
        return decorator
    return decorator(cls)
