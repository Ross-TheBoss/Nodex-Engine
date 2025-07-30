from abc import * 
from typing import * 

class AbstractTiming:
    @abstractmethod
    def __init__(self, fps) -> None:
        pass
    
    @abstractmethod
    def tick(self) -> None:
        pass 
    
    @abstractmethod
    def get_fps(self) -> int:
        pass 
    