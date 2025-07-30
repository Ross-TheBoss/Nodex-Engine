import pygame
from nodex.abstract.texture import *
from typing import *

class PygameTexture(AbstractTexture):
    def __init__(self, path: str) -> None:
        self.texture = pygame.image.load(path).convert_alpha()
        self.base_texture = self.texture.copy()
        
    def scale(self, scaling: Tuple[float, float]) -> None:
        self.texture = pygame.transform.scale(self.base_texture, (scaling[0] * self.size[0], scaling[1] * self.size[1]))
        
    def rotate(self, angle: float) -> None:
        self.texture = pygame.transform.rotate(self.base_texture, angle)
    
    @property
    def size(self):
        return self.base_texture.get_size()
    