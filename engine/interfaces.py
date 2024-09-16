from abc import ABC, abstractmethod


class GhostSprite(ABC):
    """Must have methods and properties for sprites"""

    @abstractmethod
    def draw(self, wnd) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def shift(self, dx: float = 0, dy: float = 0) -> None:
        pass

    @property
    @abstractmethod
    def sizes(self) -> tuple[float, float]:
        pass

    @property
    @abstractmethod
    def pos(self) -> tuple[float, float]:
        pass
    
    @property
    @abstractmethod
    def name(self) -> int:
        pass

    
class Interactive(ABC):
    """Must have methods for interactive entities"""
    
    @abstractmethod
    def interact(self, target) -> None:
        pass


class Transport(ABC):
    """Must have methods for transport entites"""

    @abstractmethod
    def joy_ride(self, target) -> None:
        pass


class Spawner(ABC):
    """Must have methods for spawners"""
    
    @abstractmethod
    def spawn(self):
        pass


class Musket(ABC):
    """Must have methods for guns"""
    
    @abstractmethod
    def shoot(self, collection) -> None:
        pass
    
    @abstractmethod
    def recharge(self) -> None:
        pass
