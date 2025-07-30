from nodex.abstract.texture import AbstractTexture
from typing import *
import sdl2
import sdl2.ext

class SDLTexture(AbstractTexture):
    def __init__(self, path: str):
        self.path = path
        self.surface = sdl2.ext.load_image(path)
        self.texture = None  
        self.width = self.surface.w
        self.height = self.surface.h

    def scale(self, scaling: Tuple[float, float]):
        self.width = int(self.width * scaling[0])
        self.height = int(self.height * scaling[1])
        self.surface = sdl2.ext.scale_surface(self.surface, (self.width, self.height))
        
    def rotate(self, angle: float):
        # PySDL2 ne fournit pas directement la rotation
        raise NotImplementedError("Rotation is not implemented with SDL2 in this wrapper.")
    
    @property
    def size(self):
        return (self.width, self.height)