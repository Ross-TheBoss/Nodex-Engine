import pyglet
import nodex

from collections import namedtuple
from nodex.abstract.input import AbstractInput
from nodex._private import *
from nodex.system_event.system_event import SystemEvent

Event = namedtuple("Event", ["type", "key"])

class _PygletEventDispatcher(pyglet.event.EventDispatcher):
    def __init__(self):
        self.events = []

    def on_key_press(self, symbol, modifiers):
        self.events.append(Event(nodex.KEYDOWN, symbol))

    def on_key_release(self, symbol, modifiers):
        self.events.append(Event(nodex.KEYUP, symbol))

    def on_close(self):
        self.events.append(Event(nodex.QUIT, None))

_PygletEventDispatcher.register_event_type("on_key_press")
_PygletEventDispatcher.register_event_type("on_key_release")
_PygletEventDispatcher.register_event_type("on_close")

class PygletInput(AbstractInput):
    def __init__(self):
        super().__init__()
        self._handler = _PygletEventDispatcher()

    def events(self):
        pyglet.app.platform_event_loop.step()

        for window in pyglet.app.windows:
            window: pyglet.window.Window
            window.switch_to()
            window.push_handlers(self._handler)
            window.dispatch_events()

            for event in self._handler.events:
                if event.type == nodex.KEYDOWN:
                    yield SystemEvent(nodex.KEYDOWN, key = translate_pyglet_key(event.key))
                if event.type == nodex.KEYUP:
                    yield SystemEvent(nodex.KEYUP, key = translate_pyglet_key(event.key))
                if event.type == nodex.QUIT:
                    yield SystemEvent(nodex.QUIT)