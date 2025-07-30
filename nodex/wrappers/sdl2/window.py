from nodex.abstract.window import AbstractWindow
from typing import *
import sdl2
import sdl2.ext

class SDLWindow(AbstractWindow):
    def __init__(self, size: Tuple[int, int]):
        sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
        self.size = size
        self.window = sdl2.ext.Window("SDL Window", size=size)
        self.window.show()

    def set_caption(self, caption: str):
        sdl2.SDL_SetWindowTitle(self.window.window, caption.encode('utf-8'))