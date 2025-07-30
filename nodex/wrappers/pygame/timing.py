import pygame 

from nodex.abstract.timing import AbstractTiming
from typing import * 

class PygameTiming(AbstractTiming):
    def __init__(self, fps):
        self.clock = pygame.time.Clock()
        self.fps = fps
        
    def tick(self) -> None:
        self.clock.tick(self.fps)
    
    def get_fps(self) -> int:
        return self.clock.get_fps()
    