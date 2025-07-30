import pygame
from nodex.abstract.renderer import *
from nodex.wrappers.pygame.texture import PygameTexture
from nodex.wrappers.pygame.window import PygameWindow
from typing import *

class PygameRenderer(AbstractRenderer):
    def __init__(self, window: PygameWindow):
        self.window = window
        
    def draw(self, texture: PygameTexture, position : Tuple[int, int]):
        self.window.display.blit(texture, position)
        
    def present(self):
        pygame.display.flip()
        
    def clear(self, color):
        self.window.display.fill(color)
    