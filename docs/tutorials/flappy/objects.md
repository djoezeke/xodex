---
title: Flappy Bird Objects
description: Tutorial For Creating Flappy Bird Objects/Entities.
---

## Background

```python

class Background(Image):
    """Game Background"""

    def __init__(self):
        backgrounds = [
            "assets/images/background-day.png",
            "assets/images/background-night.png",
        ]
        super().__init__(random.choice(backgrounds), (0, 0))
```

## Floor

```python

class Floor(Image):
    """Game Fooor"""

    def __init__(self, win_width):
        super().__init__("assets/images/base.png", pos=(0, int(512 * 0.79)))
        self.vel_x = 4
        self.x_extra = self.rect.width - win_width

    def perform_draw(self, surface, *args, **kwargs):
        self.rect.x = -((-self.rect.x + self.vel_x) % self.x_extra)
        return super().perform_draw(surface, *args, **kwargs)
```

## Pipe

```python

class Pipe(Image):
    def __init__(
        self, win_width, win_height, x, y, flipped: bool = False, vel_x: int = -4
    ):
        self.flipped = flipped
        self.vel_x = vel_x
        image_path = random.choice(
            ["assets/images/pipe-green.png", "assets/images/pipe-red.png"]
        )
        super().__init__(image_path, pos=(x, y))
        if flipped:
            self.flip(False, True)

    def perform_update(self, deltatime, *args, **kwargs):
        self.rect.x += self.vel_x

    def is_off_screen(self):
        return self.rect.right < 0
```

## Pipes

```python

class Pipes(DrawableObject, EventfulObject, LogicalObject):
    def __init__(
        self, win_width, win_height, gap_size=100, pipe_distance=200, vel_x=-4
    ):
        self.win_width = win_width
        self.win_height = win_height
        self.gap_size = gap_size
        self.pipe_distance = pipe_distance
        self.vel_x = vel_x
        self.upper = []
        self.lower = []
        self._spawn_pipe()

    def _spawn_pipe(self):
        # Randomize the gap position
        min_y = int(self.win_height * 0.2)
        max_y = int(self.win_height * 0.6)
        gap_y = random.randint(min_y, max_y)
        pipe_x = self.win_width + 10
        upper_pipe = Pipe(
            self.win_width,
            self.win_height,
            pipe_x,
            gap_y - self.gap_size // 2 - 320,
            True,
            self.vel_x,
        )
        lower_pipe = Pipe(
            self.win_width,
            self.win_height,
            pipe_x,
            gap_y + self.gap_size // 2,
            False,
            self.vel_x,
        )
        self.upper.append(upper_pipe)
        self.lower.append(lower_pipe)

    def perform_update(self, deltatime, *args, **kwargs):
        for pipe in self.upper + self.lower:
            pipe.perform_update(deltatime, *args, **kwargs)
        # Remove pipes that are off screen
        self.upper = [p for p in self.upper if not p.is_off_screen()]
        self.lower = [p for p in self.lower if not p.is_off_screen()]
        # Spawn new pipes if needed
        if len(self.upper) == 0 or (
            self.upper[-1].rect.x < self.win_width - self.pipe_distance
        ):
            self._spawn_pipe()

    def perform_draw(self, surface, *args, **kwargs):
        for pipe in self.upper + self.lower:
            pipe.perform_draw(surface, *args, **kwargs)

    def handle_event(self, event, *args, **kwargs):
        for pipe in self.upper + self.lower:
            pipe.handle_event(event, *args, **kwargs)
```

## 4 — Bird object (Drawable + Logical + Eventful)

Create a `Bird` by combining responsibilities. Implement draw, update and
event handling (jump on key press):

```python

class Bird(Animator):
    """
    Bird class handles the animated sprite for the player character.

    Args:
        x (int): Initial x position.
        y (int): Initial y position.
    """

    def __init__(self, x=50, y=256):
        bird_sprites = [
            [
                "assets/images/bluebird-downflap.png",
                "assets/images/bluebird-midflap.png",
                "assets/images/bluebird-upflap.png",
            ],
            [
                "assets/images/yellowbird-downflap.png",
                "assets/images/yellowbird-midflap.png",
                "assets/images/yellowbird-upflap.png",
            ],
            [
                "assets/images/redbird-downflap.png",
                "assets/images/redbird-midflap.png",
                "assets/images/redbird-upflap.png",
            ],
        ]
        super().__init__(
            random.choice(bird_sprites),
            frame_duration=100,
            loop=True,
            pingpong=False,
            reverse=False,
            on_finish=None,
            pos=(x, y),
        )

```

```python

class Flappy(DrawableObject, EventfulObject, LogicalObject):
    """
    Flappy is the main player character, handling movement, flapping, and collision.

    Args:
        x (int): Initial x position.
        y (int): Initial y position.
        floor: Floor object for collision.
        pipes: List of pipe objects for collision.
    """

    def __init__(self, win_width, win_height):
        x = int(win_width * 0.2)
        y = int((win_height - 24) / 2)
        self.flappy = Bird(x, y)

        self.min_y = -2 * self.flappy.rect.height
        self.max_y = (win_height * 0.79) - self.flappy.rect.height * 0.75

        self.crash_entity = None
        self.crashed = False
        self.set_mode(PlayerMode.SHM)

    def set_mode(self, mode: PlayerMode) -> None:
        """
        Set the current movement mode for Flappy.

        Args:
            mode (PlayerMode): The mode to set.
        """
        self.mode = mode
        if mode == PlayerMode.NORMAL:
            self.reset_vals_normal()
            Sounds().play("wing")
        elif mode == PlayerMode.SHM:
            self.reset_vals_shm()
        elif mode == PlayerMode.CRASH:
            Sounds().play("hit")
            if self.crash_entity == "pipe":
                Sounds().play("die")
            self.reset_vals_crash()

    def reset_vals_crash(self) -> None:
        self.acc_y = 2
        self.vel_y = 7
        self.max_vel_y = 15
        self.vel_rot = -8

    def reset_vals_normal(self) -> None:
        """Reset physics values for normal gameplay."""
        self.vel_y = -9
        self.max_vel_y = 10
        self.min_vel_y = -8
        self.acc_y = 1
        self.rot = 80
        self.vel_rot = -3
        self.rot_min = -90
        self.rot_max = 20
        self.flap_acc = -9
        self.flapped = False

    def reset_vals_shm(self) -> None:
        """Reset physics values for simple harmonic motion (idle)."""
        self.vel_y = 1
        self.max_vel_y = 4
        self.min_vel_y = -4
        self.acc_y = 0.5

        self.rot = 0
        self.vel_rot = 0
        self.rot_min = 0
        self.rot_max = 0

        self.flap_acc = 0
        self.flapped = False

    def flap(self) -> None:
        """
        Make the bird flap if possible.
        Only works if not in CRASH mode and not at the top of the screen.
        """
        if self.mode == PlayerMode.CRASH:
            return
        if self.flappy.rect.y > self.min_y:
            self.vel_y = self.flap_acc
            self.flapped = True
            # Instantly rotate up on flap
            self.rot = self.rot_max
            Sounds().play("wing")

    def tick_normal(self) -> None:
        """Update position and rotation for normal gameplay mode."""
        if self.vel_y < self.max_vel_y and not self.flapped:
            self.vel_y += self.acc_y
        if self.flapped:
            self.flapped = False

        self.flappy.rect.y = clamp(
            self.flappy.rect.y + self.vel_y, self.min_y, self.max_y
        )

        # Rotate up on flap, then smoothly rotate down as falling
        if self.vel_y < 0:
            self.rot = self.rot_max
        else:
            self.rotate()

    def rotate(self) -> None:
        """Rotate smoothly"""
        self.rot += self.vel_rot
        if self.rot < self.rot_min:
            self.rot = self.rot_min
        elif self.rot > self.rot_max:
            self.rot = self.rot_max

    def tick_crash(self) -> None:
        """Update position and rotation for crash mode."""
        if self.min_y <= self.flappy.rect.y <= self.max_y:
            self.flappy.rect.y = clamp(
                self.flappy.rect.y + self.vel_y, self.min_y, self.max_y
            )
            # Rotate only when it's a pipe crash and bird is still falling
            if self.crash_entity != "floor":
                self.rotate()

        # player velocity change
        if self.vel_y < self.max_vel_y:
            self.vel_y += self.acc_y

    def tick_shm(self) -> None:
        """Update position for idle (SHM) mode."""
        if self.vel_y >= self.max_vel_y or self.vel_y <= self.min_vel_y:
            self.acc_y *= -1
        self.vel_y += self.acc_y
        self.flappy.rect.y += self.vel_y

    def collided(self, floor, pipes) -> bool:
        """
        Check for collision with the floor or pipes.

        Returns:
            bool: True if collision detected, else False.
        """

        # Floor collision
        if self.collide(floor.rect):
            self.crashed = True
            self.crash_entity = "floor"
            return True

        # Pipes collision
        for pipe in pipes.upper:
            if self.collide(pipe.rect):
                self.crashed = True
                self.crash_entity = "pipe"
                return True

        for pipe in pipes.lower:
            if self.collide(pipe.rect):
                self.crashed = True
                self.crash_entity = "pipe"
                return True

        return False

    def collide(self, other) -> bool:
        """collide"""
        return self.flappy.rect.colliderect(other)

    def crossed(self, pipe) -> bool:
        """Return True if Flappy has just crossed a pipe (for scoring)."""
        # Check if Flappy's x just passed the pipe's x (from right to left)
        return (
            pipe.rect.right < self.flappy.rect.left
            and pipe.rect.right >= self.flappy.rect.left + pipe.vel_x
        )

    def perform_draw(self, surface, *args, **kwargs):
        """
        Draw Flappy on the given surface.

        Args:
            surface: Pygame surface.
        """

        image = self.flappy.get_image()
        rotated_image = pygame.transform.rotate(image.image, self.rot)
        rotated_rect = rotated_image.get_rect(center=self.flappy.rect.center)
        surface.blit(rotated_image, rotated_rect)

    def handle_event(self, event: Event, *args, **kwargs) -> None:
        """
        Handle an event for Flappy.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        self.flappy.handle_event(event, *args, **kwargs)

    def perform_update(self, deltatime: float, *args, **kwargs) -> None:
        """
        Update Flappy's state.

        Args:
            deltatime (float): Time since last update in seconds.
        """

        if self.mode == PlayerMode.SHM:
            self.tick_shm()
        elif self.mode == PlayerMode.NORMAL:
            self.tick_normal()
        elif self.mode == PlayerMode.CRASH:
            self.tick_crash()

        self.flappy.perform_update(deltatime, *args, **kwargs)

```

```python
class Score(DrawableObject):
    """Game Score

    Simple score display that composes digit `Image` objects and plays a
    sound when the player earns a point.
    """

    def __init__(self, win_width, win_height):
        # load digit images 0-9
        self.numbers = [Image(f"assets/images/{i}.png") for i in range(10)]

        self.width = win_width
        self.height = win_height

        self.y = int(win_height * 0.1)
        self.score = 0

    def set(self, score: int) -> None:
        """Set Score"""
        self.score = score

    def reset(self) -> None:
        """Reset Score"""
        self.score = 0

    def add(self) -> None:
        """Increase Score"""
        self.score += 1
        # Use the engine sound helper; guard if sound is missing
        try:
            Sounds().play("point")
        except Exception:
            # don't crash the game for missing/misconfigured audio
            pass

    def perform_draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        """Draw the score centered at the top of the screen."""
        score_digits: list[int] = [int(x) for x in list(str(self.score))]
        images: list[Image] = [self.numbers[digit] for digit in score_digits]
        digits_width = sum(image.rect.width for image in images)
        x_offset = (self.width - digits_width) // 2

        for image in images:
            surface.blit(image.image, (x_offset, self.y))
            x_offset += image.rect.width

    @property
    def rect(self) -> pygame.Rect:
        """Bounding rect for layout/collision (useful for scene positioning)."""
        score_digits: list[int] = [int(x) for x in list(str(self.score))]
        images: list[Image] = [self.numbers[digit] for digit in score_digits]
        w = sum(image.rect.width for image in images)
        x = (self.width - w) // 2
        h = max(image.rect.height for image in images)
        return pygame.Rect(x, self.y, w, h)

```

## 5 — Pipes and collision

Implement a simple `PipeManager` that yields pipe pairs, moves them left, and
checks collision with the `Bird`. On collision, call scene's `pause()` or
transition to a Game Over scene.

Notes and tips

- Physics: the example above mostly uses discrete integer velocities (matching
  the original Flappy feel). If your engine uses variable FPS, multiply
  accelerations and position changes by `deltatime` (seconds) for stable
  physics.
- Collision: use `pygame.Rect`'s `colliderect` for simple AABB collisions.
  If you need pixel-perfect collision, consider masks but only if necessary.
- Sound: wrap calls to `Sounds().play()` in a try/except when running in
  headless or CI environments to avoid crashes caused by missing audio drivers.

```python

```

## 6 — Scoring and polish

```python
class Score(DrawableObject):
    """Game Score"""

    def __init__(self, win_width, win_height):
        self.numbers = [
            Image("assets/images/0.png"),
            Image("assets/images/1.png"),
            Image("assets/images/2.png"),
            Image("assets/images/3.png"),
            Image("assets/images/4.png"),
            Image("assets/images/5.png"),
            Image("assets/images/6.png"),
            Image("assets/images/7.png"),
            Image("assets/images/8.png"),
            Image("assets/images/9.png"),
        ]

        self.width = win_width
        self.height = win_height

        self.y = win_height * 0.1
        self.score = 0

    def set(self, score: int) -> None:
        """Set Score"""
        self.score = score

    def reset(self) -> None:
        """Reset Score"""
        self.score = 0

    def add(self) -> None:
        """Increase Score"""
        self.score += 1
        pygame.mixer.Sound("assets/sounds/point.wav").play()

    def perform_draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        """
        Actual drawing logic. Must be implemented by subclass.

        Args:
            surface (Surface): The Pygame surface to draw on.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        score_digits: list[int] = [int(x) for x in list(str(self.score))]
        images: list[Image] = [self.numbers[digit] for digit in score_digits]
        digits_width = sum(image.rect.width for image in images)
        x_offset = (self.width - digits_width) / 2

        for image in images:
            surface.blit(image.image, (x_offset, self.y))
            x_offset += image.rect.width

    @property
    def rect(self) -> pygame.Rect:
        """rect"""
        score_digits: list[int] = [int(x) for x in list(str(self.score))]
        images: list[Image] = [self.numbers[digit] for digit in score_digits]
        w = sum(image.rect.width for image in images)
        x = (self.width - w) / 2
        h = max(image.rect.height for image in images)
        return pygame.Rect(x, self.y, w, h)

```

- Count pipes passed for score.
- Add sound effects using `xodex.game.sounds.Sounds`.
- Use `Scene.export_image()` to create screenshots for debugging.
