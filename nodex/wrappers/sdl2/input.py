import sdl2
import sdl2.ext 
import nodex
from nodex.abstract.input import AbstractInput
from nodex.system_event.system_event import SystemEvent

class SDL2Input(AbstractInput):
    def events(self):
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                yield SystemEvent(nodex.QUIT)