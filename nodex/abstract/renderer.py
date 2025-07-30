from abc import * 
from typing import *
from nodex.abstract.texture import *
from nodex.abstract.window import *

class AbstractRenderer(ABC):
    def __init__(self, target: AbstractWindow):
        self.target = target
        
    @abstractmethod
    def draw(self, texture: AbstractTexture, position : Tuple[int, int]):
        pass
    
    @abstractmethod
    def present(self):
        pass
    
    @abstractmethod
    def clear(self, color: Tuple[int, int]):
        pass
    
    
    