import pygame
import sys
import time
from typing import Callable, Any

from engine.colors import *
from engine.events import *
from engine._private import *
from engine.event.event import Event


class Context:
    """
    The Context manages the game's rendering surface, event system, timing, and core loop.

    It serves as the central interface to the game engine's state, handling:
    - Display rendering
    - Time management
    - Input events
    - Event queue
    - Game loop execution
    """

    def __init__(self, resolution: tuple[int, int], flags: int = 0, vsync: bool = True, fps: int = 10000):
        """
        Initializes the game context.

        Args:
            resolution (tuple[int, int]): The resolution of the display (width, height).
            flags (int, optional): Optional display flags for pygame (e.g., pygame.FULLSCREEN).
            vsync (bool, optional): Whether to enable vertical sync.
            fps (int, optional): Maximum frame rate (used to cap the loop speed).
        """
        self.screen: pygame.Surface = pygame.display.set_mode(resolution, flags, vsync=vsync)
        self.display: pygame.Surface = self.create_surface(resolution)
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.camera: list[int] = [0, 0]
        self.fps: int = fps
        self.lt: float = time.perf_counter()
        self.dt: float = 1.0
        self.events: list[Event] = []
        self.keyboard: Any = None

    def push_event(self, type: str, **kwargs) -> None:
        """
        Push a custom event into the internal event queue.

        Args:
            type (str): The type of the event.
            **kwargs: Arbitrary data to attach to the event.
        """
        self.events.append(Event(type, **kwargs))

    def delta_time(self) -> None:
        """
        Update the delta time (dt) based on the time elapsed since the last frame.

        Multiplies by 60 to normalize against a 60 FPS reference.
        """
        self.dt = (time.perf_counter() - self.lt) * 60
        self.lt = time.perf_counter()

    def pygame_events(self) -> None:
        """
        Handle Pygame native events and translate them into the engine's event system.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            if event.type == pygame.KEYDOWN:
                self.push_event(KEYDOWN, key=translate_pygame_key(event.key))

    def run(self, game_loop: Callable[[], None]) -> None:
        """
        Start the main game loop.

        Args:
            game_loop (Callable): A function that contains the game logic to be executed each frame.
        """
        while True:
            self.delta_time()
            self.pygame_events()
            self.keyboard = pygame.key.get_pressed()
            self.display.fill(BLACK)
            game_loop()
            self.screen.blit(self.display, (0, 0))
            pygame.display.flip()
            self.clock.tick(self.fps)
            self.events.clear()

    def loop(self) -> Callable[[Callable[[], None]], None]:
        """
        Decorator to wrap a function as the main game loop.

        Returns:
            Callable: A decorator that launches the main loop.
        """
        def wrapper(game_loop: Callable[[], None]) -> None:
            self.run(game_loop)
        return wrapper

    def exit(self) -> None:
        """
        Exit the game cleanly.
        """
        pygame.quit()
        sys.exit()

    def load_image(self, path: str) -> pygame.Surface:
        """
        Load an image from the given path.

        Args:
            path (str): Path to the image file.

        Returns:
            pygame.Surface: The loaded image.
        """
        return pygame.image.load(path)

    def draw(self, surface: pygame.Surface, position: tuple[int, int], relative: bool = False) -> None:
        """
        Draw a surface on the display.

        Args:
            surface (pygame.Surface): The image or surface to draw.
            position (tuple[int, int]): The position to draw it at.
            relative (bool): If True, apply the camera offset.
        """
        if relative:
            self.display.blit(surface, (position[0] - self.camera[0], position[1] - self.camera[1]))
        else:
            self.display.blit(surface, position)

    def create_surface(self, size: tuple[int, int]) -> pygame.Surface:
        """
        Create a new surface with the given size.

        Args:
            size (tuple[int, int]): The width and height of the surface.

        Returns:
            pygame.Surface: A new surface object.
        """
        return pygame.Surface(size)
