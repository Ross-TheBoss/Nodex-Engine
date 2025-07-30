from nodex.wrappers.pygame.window import * 
from nodex.wrappers.pygame.renderer import * 
from nodex.wrappers.pygame.texture import * 
from nodex.abstract.context import *

class Context(AbstractContext):
    def __init__(self, size):
        self.window = PygameWindow(size)
        self.renderer = PygameRenderer(self.window)
        
    def delta_time(self) -> None:
        REFERENCE_FPS = 60
        self.dt = (time.perf_counter() - self.lt) * REFERENCE_FPS
        self.lt = time.perf_counter()
        
    def loop(self) -> Callable[[Callable[[], None]], None]:
        def wrapper(game_loop: Callable[[], None]) -> None:
            self.run(game_loop)
        return wrapper
  
    def run(self, game_loop: Callable[[], None]) -> None:
        while True:
            self.delta_time()
            game_loop()
            self.renderer.present()    
            self.renderer.clear()

            