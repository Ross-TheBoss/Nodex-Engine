import pygame 
import nodex

from nodex.abstract.input import AbstractInput
from nodex._private import *
from nodex.system_event.system_event import SystemEvent

class PygameInput(AbstractInput):
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                yield SystemEvent(nodex.KEYDOWN, key = translate_pygame_key(event.key))
            if event.type == pygame.KEYUP:
                yield SystemEvent(nodex.KEYUP, key = translate_pygame_key(event.key))
            if event.type == pygame.QUIT:
                yield SystemEvent(nodex.QUIT)