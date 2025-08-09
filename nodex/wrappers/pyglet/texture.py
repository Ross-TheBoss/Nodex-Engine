import pyglet
from nodex.abstract.texture import *
from typing import *


class PygletTexture(AbstractTexture):
    def __init__(self, path: str) -> None:
        self.texture = pyglet.image.load(path)
        self.sprite = pyglet.sprite.Sprite(self.texture)

    def scale(self, scaling: Tuple[float, float]) -> None:
        self.sprite.scale_x = scaling[0]
        self.sprite.scale_y = scaling[1]

    def rotate(self, angle: float) -> None:
        self.sprite.rotation = angle

    @property
    def size(self):
        return self.texture.width, self.texture.height