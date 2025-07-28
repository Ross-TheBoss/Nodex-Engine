import pygame, sys, time, os

from engine.colors import *

class Context:
    def __init__(self, resolution, flags = 0, vsync = True, fps=10000):
        self.screen = pygame.display.set_mode(resolution, flags, vsync=vsync)
        self.display = self.create_surface(resolution)
        self.clock = pygame.time.Clock()
        self.camera = [0, 0]
        self.fps = fps
        self.lt = time.perf_counter()
        
    def delta_time(self):
        self.dt = (time.perf_counter() - self.lt) * 60 
        self.lt = time.perf_counter()
        
    def pygame_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit() 
        
    def run(self, game_loop):
        while True: 
            self.delta_time()
            self.pygame_events()
            self.keyboard = pygame.key.get_pressed()
            self.display.fill(BLACK)
            game_loop()
            self.screen.blit(self.display, (0, 0))
            pygame.display.flip()
            self.clock.tick(self.fps)
            
    def loop(self):
        def wrapper(game_loop):
            self.run(game_loop)
        return wrapper
            
    def exit(self):
        pygame.quit()
        sys.exit()
        
    def load_image(self, path):
        return pygame.image.load(path)
    
    def draw(self, surface, position, relative = False):
        if relative:
            self.display.blit(surface, (position[0] - self.camera[0], position[1] - self.camera[1]))
        else:
            self.display.blit(surface, position)        
            
    def create_surface(self, size):
        return pygame.Surface(size)
    