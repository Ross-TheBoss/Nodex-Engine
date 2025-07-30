import time
from abc import *
from typing import *
from nodex.abstract.renderer import * 


class AbstractContext(ABC):
    
    def delta_time(self) -> None:
        REFERENCE_FPS = 60
        self.dt = (time.perf_counter() - self.lt) * REFERENCE_FPS
        self.lt = time.perf_counter()
        
    def loop(self) -> Callable[[Callable[[], None]], None]:
        def wrapper(game_loop: Callable[[], None]) -> None:
            self.run(game_loop)
        return wrapper
    
    @property
    def fps(self) -> float:
        pass 
    
    @property
    def dt(self) -> float:
        pass 
    
    @property
    def renderer(self) -> AbstractRenderer:
        return self._renderer
        
    @abstractmethod
    def run(self, game_loop: Callable[[], None]) -> None:
        pass 
    
