import nodex
import sys
import time
from nodex.wrappers.pygame.window import * 
from nodex.wrappers.pygame.renderer import * 
from nodex.wrappers.pygame.texture import * 
from nodex.wrappers.pygame.timing import *
from nodex.wrappers.pygame.input import *
from nodex.wrappers.sdl2.window import * 
from nodex.wrappers.sdl2.renderer import * 
from nodex.wrappers.sdl2.texture import * 
from nodex.wrappers.sdl2.timing import *
from nodex.wrappers.sdl2.input import *
from typing import *

DEFAULT_BACKEND = "pygame"
REFERENCE_FPS = 60
class Context:
    def __init__(self, size: Tuple[int, int], backend: str = DEFAULT_BACKEND) -> None:
        self.backend: str = backend
        self.init_backend(size)
        self.window.set_caption('Nodex Project')
        self.lt: float = time.perf_counter()
        self._dt: float = 1
    
    @property 
    def texture_type(self) -> AbstractTexture:
        return {
            "pygame" : PygameTexture,
            "sdl2" : SDLTexture
        }[self.backend]
    
    def init_backend(self, size: Tuple[int, int]) -> None:
        if self.backend == "pygame":
            self.window = PygameWindow(size)
            self.renderer = PygameRenderer(self.window)
            self.timer = PygameTiming(10000)
            self.input = PygameInput()
        elif self.backend == "sdl2":
            self.window = SDLWindow(size)
            self.renderer = SDLRenderer(self.window)
            self.timer = SDLTiming(10000)
            self.input = SDL2Input()
        else:
            raise ValueError(f"Backend {self.backend} not known.")
            
    def delta_time(self) -> None:
        self._dt = (time.perf_counter() - self.lt) * REFERENCE_FPS
        self.lt = time.perf_counter()
        
    def loop(self) -> Callable[[Callable[[], None]], None]:
        def wrapper(game_loop: Callable[[], None]) -> None:
            self.run(game_loop)
        return wrapper
  
    def run(self, game_loop: Callable[[], None]) -> None:
        while True:
            for event in self.input.events():
                if event.type == nodex.QUIT:
                    self.window.close()
                    self.quit()
            self.delta_time()
            self.renderer.clear(nodex.BLACK)
            game_loop()
            self.renderer.present()    
            self.timer.tick()
           
    def quit(self) -> None:
        sys.exit()
        
    @property
    def fps(self) -> int:
        return self.timer.get_fps()
    
    @property
    def dt(self) -> float:
        return self._dt
    
    def load_texture(self, path: str) -> None:
        return self.texture_type(path)
    
    def draw(self, texture: AbstractTexture, position: Tuple[int, int]) -> None:
        self.renderer.draw(texture, position)

            