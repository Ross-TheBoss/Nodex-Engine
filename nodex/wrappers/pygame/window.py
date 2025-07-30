import pygame 
from nodex.abstract.window import AbstractWindow
from typing import *

class PygameWindow(AbstractWindow):
    def __init__(self, size: Tuple[int, int]):
        self.display = pygame.display.set_mode(size)
    def set_caption(self, caption: str) -> None:
        pygame.display.set_caption(caption)
    def close(self):
        pygame.quit()
        