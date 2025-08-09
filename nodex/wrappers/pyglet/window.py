import pyglet
from nodex.abstract.window import AbstractWindow
from typing import *

class PygletWindow(AbstractWindow):
    def __init__(self, size: Tuple[int, int]):
        self.display = pyglet.window.Window(width=size[0], height=size[1], vsync=False)

    def set_caption(self, caption: str) -> None:
        self.display.set_caption(caption)

    def close(self):
        self.display.close()