from abc import ABC, abstractmethod


class Scene(ABC):
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self, screen):
        pass
