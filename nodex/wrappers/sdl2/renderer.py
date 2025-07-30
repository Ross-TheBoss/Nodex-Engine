from nodex.abstract.renderer import AbstractRenderer
from nodex.abstract.window import AbstractWindow
from nodex.wrappers.sdl2.texture import SDLTexture
from typing import *
import sdl2
import sdl2.ext

class SDLRenderer(AbstractRenderer):
    def __init__(self, target: AbstractWindow):
        super().__init__(target)
        self.renderer = sdl2.ext.Renderer(target.window)
        self.factory = sdl2.ext.SpriteFactory(renderer=self.renderer)

    def draw(self, texture: SDLTexture, position: Tuple[int, int]):
        if texture.texture is None:
            texture.texture = self.factory.from_surface(texture.surface)
        texture.texture.position = position
        self.renderer.copy(texture.texture)

    def present(self):
        self.renderer.present()

    def clear(self, color: Tuple[int, int]):
        self.renderer.clear(sdl2.ext.Color(*color))