from abc import * 

class AbstractInput:
    @abstractmethod
    def events(self):
        pass        