from nodex.abstract.timing import AbstractTiming
from typing import *
import sdl2
import sdl2.ext

import time

class SDLTiming(AbstractTiming):
    def __init__(self, fps):
        self.fps = fps
        self.frame_duration = 1.0 / fps
        self.last_time = time.perf_counter()
        self._actual_fps = fps  # estimation simple

    def tick(self):
        now = time.perf_counter()
        elapsed = now - self.last_time
        delay = self.frame_duration - elapsed

        if delay > 0:
            time.sleep(delay)
            now = time.perf_counter()
            elapsed = now - self.last_time

        self._actual_fps = 1.0 / max(elapsed, 1e-8)
        self.last_time = now

    def get_fps(self) -> int:
        return int(self._actual_fps)