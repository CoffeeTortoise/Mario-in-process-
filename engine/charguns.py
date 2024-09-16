from engine.gun import ParabolaGun
from engine.enumerations import EntityName
from engine.interfaces import Spawner
from engine.constants import Sizes


SIZE: float = Sizes().size


class SpawnerFiregun(Spawner):
    """Caused by a fire flower"""
    def __init__(self, right: bool, equiped: bool, time_charge: float = .5) -> None:
        self._bullet_image: str = 'Assets/Sprites/Characters/Polys/Mario/Fire/5.bmp'
        self._bullet_sizes: tuple[float, float] = SIZE * .25, SIZE * .25
        self._time_charge: float = time_charge
        self._bullet_fly_angle: float = 100
        self._bullets: int = 10
        self._bullet_damage: int = 2
        self._bullet_enemy_name: int = EntityName.monster
        self._right: bool = right
        self._equiped: bool = equiped
    
    def spawn(self) -> ParabolaGun:
        return ParabolaGun(self._bullet_image, self._bullet_sizes, self._bullet_fly_angle, self._bullets,
                           self._time_charge, bullet_damage=self._bullet_damage,
                           bullet_enemy_name=self._bullet_enemy_name,
                           bullet_physical=False, equiped=self._equiped, right=self._right)
    
    def __del__(self) -> None:
        pass
