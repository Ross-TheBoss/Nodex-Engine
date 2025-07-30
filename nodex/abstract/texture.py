from abc import * 
from typing import *

class AbstractTexture(ABC):
    @abstractmethod
    def __init__(self, path: str) -> None:
        pass 
    def slice(self, slicing: Tuple[int, int]) -> None:
        pass 
    @abstractmethod
    def scale(self, scaling: Tuple[float, float]) -> None:
        pass
    @abstractmethod
    def rotate(self, angle: float) -> None:
        pass
    
    @property
    def size(self):
        pass