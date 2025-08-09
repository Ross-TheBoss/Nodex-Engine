import pyglet

from nodex.abstract.timing import AbstractTiming

class PygletTiming(AbstractTiming):
    def __init__(self, fps):
        self.clock = pyglet.clock.Clock()
        self.fps = fps
        
    def tick(self) -> None:
        self.clock.tick(self.fps)
    
    def get_fps(self) -> int:
        return int(self.clock.get_frequency())
    