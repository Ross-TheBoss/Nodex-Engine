from nodex.abstract.renderer import *
from nodex.wrappers.pyglet.texture import PygletTexture
from nodex.wrappers.pyglet.window import PygletWindow
from typing import *


class PygletRenderer(AbstractRenderer):
    def __init__(self, window: PygletWindow):
        self.window = window

    def draw(self, texture: PygletTexture, position: Tuple[int, int]):
        # Invert the y-coordinate for pyglet
        texture.sprite.update(x=position[0], y=self.window.display.height - texture.texture.height - position[1])
        texture.sprite.draw()

    def present(self):
        self.window.display.flip()

    def clear(self, color):
        self.window.display.clear()