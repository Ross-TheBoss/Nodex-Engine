from abc import * 
from typing import *

class AbstractWindow(ABC):
    @abstractmethod
    def __init__(self, size: Tuple[int, int]):
        pass