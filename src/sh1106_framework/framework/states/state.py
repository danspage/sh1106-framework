from abc import ABC, abstractmethod

class State(ABC):
    initialized = False
    
    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def render(self):
        pass