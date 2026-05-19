from abc import ABC, abstractmethod

class Player(ABC):
    @property
    @abstractmethod
    def age(self): pass

    @property
    @abstractmethod
    def energy(self): pass

    @property
    @abstractmethod
    def health(self): pass

    @property
    @abstractmethod
    def hunger(self): pass

    @property
    @abstractmethod
    def mood(self): pass

    @property
    @abstractmethod
    def potty(self): pass

    @abstractmethod
    def player_eats(self, food): pass

    @abstractmethod
    def player_moves(self): pass

    @abstractmethod
    def player_plays(self): pass

    @abstractmethod
    def player_sleeps(self): pass

    @abstractmethod
    def player_poops(self): pass
