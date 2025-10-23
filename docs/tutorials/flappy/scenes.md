---
title: Flappy Bird Scenes
description: Tutorial For Creating Flappy Bird Scenes.
---

## Game Home Scene

```python
class MainScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _generate_objects_(self):
        Bird = self.object.Bird
        Image = self.object.Image
        Floor = self.object.Floor
        Flappy = self.object.Flappy
        Background = self.object.Background

        message = Image(
            "assets/images/message.png",
            (int((self.width - 184) // 2), int(self.height * 0.12)),
        )

        yield Background()
        yield Floor(self.width)
        yield Bird(120, 120)
        yield Flappy(self.width, self.height)
        yield message

    def handle_scene(self, event: Event, *args, **kwargs) -> None:
        """
        Handle an event for all objects in the scene.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.entergame()
        super().handle_scene(event, *args, **kwargs)

    def entergame(self):
        """entergame"""
        # self.sounds.play("wing")
        self.manager.reset("GameScene")

    # Notes:
    # - `_generate_objects_` is called by the Scene manager when the scene is
    #   created or reset. Use it to yield live instances of objects that the
    #    scene should manage.
    # - To preload sounds or resources, use `on_first_enter` or `on_enter` if
    #   your scene system supports those hooks.
```

## Game Play Scene

```python

class GameScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        Pipes = self.object.Pipes
        Floor = self.object.Floor
        Score = self.object.Score
        Flappy = self.object.Flappy

        self.floor = Floor(self.width)
        self.score = Score(self.width, self.height)
        self.pipes = Pipes(self.width, self.height)
        self.flappy = Flappy(self.width, self.height)

    def _generate_objects_(self):
        Background = self.object.Background

        self.flappy.set_mode(2)  # normal mode

        yield Background()
        yield self.floor
        yield self.pipes
        yield self.score
        yield self.flappy

    def gameover(self):
        """entergame"""
        # self.sounds.play("die")
        self.manager.append("OverScene", self.screen, self.score.score)

    def is_tap_event(self, event) -> bool:
        """
        Determine if the event is a flap/tap event.

        Args:
            event: Pygame event.

        Returns:
            bool: True if event is a tap/flap.
        """
        m_left, _, _ = pygame.mouse.get_pressed()
        space_or_up = event.type == pygame.KEYDOWN and (
            event.key == pygame.K_SPACE or event.key == pygame.K_UP
        )
        screen_tap = event.type == pygame.FINGERDOWN
        return m_left or space_or_up or screen_tap

    def handle_scene(self, event: Event, *args, **kwargs) -> None:
        """
        Handle an event for all objects in the scene.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        if self.is_tap_event(event):
            self.flappy.flap()
        super().handle_scene(event, *args, **kwargs)

    def update_scene(self, deltatime: float, *args, **kwargs) -> None:
        """
        Update all objects in the scene, unless paused.

        Args:
            deltatime (float): Time since last update (ms).
        """

        # Collision check first: when collided, transition to game over.
        if self.flappy.collided(self.floor, self.pipes):
            # play sounds safely
            try:
                self.sounds.play("hit")
            except Exception:
                pass
            self.gameover()

        # Score: when flappy crosses a pipe, increment score. Use a copy of
        # the pipe list so modifications during iteration are safe.
        for pipe in list(self.pipes.upper):
            if self.flappy.crossed(pipe):
                self.score.add()

        # Continue with default update to tick and draw children
        super().update_scene(deltatime, *args, **kwargs)
```

## Game Over Scene

```python

class OverScene(BlurScene):
    def __init__(self, blur_surface, score, **kwargs):
        super().__init__(
            blur_surface, blur_count=2, blur_duration=3, on_blur_complete=None, **kwargs
        )
        self.score = score

    def _generate_objects_(self):
        Image = self.object.Image
        Score = self.object.Score

        score = Score(self.width, self.height)
        score.set(self.score)

        message = Image(
            "assets/images/gameover.png",
            (int((self.width - 184) // 2), int(self.height * 0.5)),
        )

        yield message
        yield score

    def handle_scene(self, event: Event, *args, **kwargs) -> None:
        """
        Handle an event for all objects in the scene.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.gotomain()
        super().handle_scene(event, *args, **kwargs)

    def gotomain(self):
        """gotomain"""
        # self.sounds.play("wing")
        self.manager.reset("MainScene")

    def on_first_enter(self, *args, **kwargs):
        # self.sounds.play("swoosh")
        pass

# Scene lifecycle & tips
- Scene creation: `_generate_objects_` should yield new instances when the
# scene is first created. Keep scene state (like score) on the scene instance
# if it needs to persist between resets.
- Event handling: call `super().handle_scene()` to ensure child objects
# receive events. Use `is_tap_event` to centralize input mapping (mouse, key,
# touch).
- Audio: use the engine `Sounds()` helper and guard in case audio fails in
# headless environments.
```
