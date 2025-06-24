from pygame import Surface

from xodex.utils.values import Values
from xodex.core.singleton import Singleton
from xodex.scenes.base_scene import BaseScene
from xodex.contrib.mainscene import XodexMainScene
from xodex.core.exceptions import NotRegistered, AlreadyRegistered, SceneError

try :
    import pygameui
    HAS_PYGAMEUI = True
except ImportError:
    HAS_PYGAMEUI = False

if HAS_PYGAMEUI:
    from xodex.contrib.pygameui.uiscene import XodexUIScene

__all__ = ("SceneManager", "register")


class SceneManager(Singleton):
    """Scene Manager with stack navigation, transitions, and scene lookup."""

    def __init__(self):

        self.__scene_classes: dict[str, BaseScene] = {}

        # for Rendering scenes
        self.__scenes: list[BaseScene] = []

        # Register default scenes
        self.register(XodexMainScene, "XodexMainScene")
        
        if HAS_PYGAMEUI:
            self.register(XodexUIScene, "XodexUIScene")

    def __contains__(self, key: str) -> bool:
        return key in self.__scene_classes.keys()

    def __len__(self) -> int:
        return len(self.__scenes)

    # region Public

    @property
    def scene(self):
        """Return Scen"""
        return self.get_scenes()

    @property
    def current(self) -> BaseScene:
        """Current scene."""
        try:
            return self.__scenes[-1]
        except IndexError:
            print("List of scenes is empty")

    def get_scene(self, scene_name: str) -> BaseScene:
        """Get a registered scene class by name."""
        return self._get_scene_(scene_name)

    def get_scenes(self) -> Values:
        """Get All Scenes."""
        return Values(self.__scene_classes)

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
        self._on_scene_exit_()
        self.__scenes.append(scene)
        self._setup_scene_()
        self._on_scene_first_enter_()

    def pop(self) -> BaseScene:
        """Pop the current scene and return it."""
        self._on_scene_last_exit_()
        pop_scene = self.__scenes.pop()
        self._on_scene_enter_()
        return pop_scene

    def clear(self):
        """Remove all scenes."""
        self.__scenes.clear()
        self.__scene_classes.clear()

    def play(self, name: str) -> None:
        """Play a Scene."""
        self._on_scene_exit_()
        scene = self._get_scene_(name)
        scene.setup()
        scene().on_first_enter()
        return scene()

    def reset(self, scene: BaseScene) -> None:
        """Replace all scenes with a new one."""
        for s in self.__scenes:
            s.on_last_exit()
        self.__scenes = [scene]
        self._setup_scene_()
        self._on_scene_first_enter_()

    def transition_to(
        self,
        new_scene: BaseScene,
        transition_type: str = "fade",
        duration: float = 1.0,
    ):
        """Transition to a new scene with an effect."""
        if transition_type == "fade":
            self._fade_transition(new_scene, duration)
        else:
            self.append(new_scene)

    def _fade_transition(self, new_scene: BaseScene, duration: float):
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
        self.append(new_scene)

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

        if issubclass(scene_class, BaseScene):
            if self.isregistered(scene_class):
                msg = "The Scene %s is already registered "
                raise AlreadyRegistered(msg)

            self.__scene_classes[scene_name] = scene_class
        else:
            msg = "The Scene %s is not of type Scene."
            raise SceneError(msg)

    def unregister(self, scene_name: str) -> None:
        """unregister a Scene Class"""
        if not self.is_registered(scene_name):
            raise NotRegistered(f"The Scene {scene_name} is not registered")
        del self.__scene_classes[scene_name]

    def isregistered(self, scene_name: str) -> bool:
        """Return true if Scene is registered"""
        return scene_name in self.__scene_classes

    # endregion

    # region Private

    def _get_scene_(self, scene_name: str) -> BaseScene:
        """Get a registered scene class by name."""
        scene = self.__scene_classes.get(scene_name)
        if scene is not None:
            return scene
        raise KeyError(f"{scene_name} is not a valid Scene")

    def _setup_scene_(self, *args, **kwargs) -> None:
        """Run if Exiting Scene. Call on_exit on current scene."""
        if self.__scenes:
            self.current.setup(*args, **kwargs)

    # endregion

    # region Hooks

    def _on_scene_exit_(self, *args, **kwargs) -> None:
        """Run if Exiting Scene. Call on_exit on current scene."""
        if self.__scenes:
            self.current.on_exit(*args, **kwargs)

    def _on_scene_last_exit_(self, *args, **kwargs) -> None:
        """Run if Reseting(Deleting) Scene. Call on_last_exit on current scene."""
        if self.__scenes:
            self.current.on_last_exit(*args, **kwargs)

    def _on_scene_enter_(self, *args, **kwargs) -> None:
        """Run if Entering Scene. Call on_enter on current scene."""
        if self.__scenes:
            self.current.on_enter(*args, **kwargs)

    def _on_scene_first_enter_(self, *args, **kwargs) -> None:
        """Run if Creating(Appending) Scene. Call on_first_enter on current scene."""
        if self.__scenes:
            self.current.on_first_enter(*args, **kwargs)

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
        scene_name = name or scene_cls.__class__.__name__
        SceneManager().register(scene_cls, scene_name)
        return scene_cls

    if cls is None:
        return decorator
    return decorator(cls)
