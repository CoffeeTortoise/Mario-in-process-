from engine.spawner import SpawnerClassicBullet, SpawnerParabolaBullet
from engine.interfaces import Musket
from engine.tools import Timer


class ClassicGun(Musket):
    def __init__(self, bullet_image_path: str,
                 bullet_sizes: tuple[float, float],
                 bullets: int = 10,
                 time_charge: int = 1,
                 bullet_damage: int = 1,
                 bullet_enemy_name: int = 0,
                 bullet_life_time: float = 8,
                 bullet_physical: bool = True,
                 equiped: bool = True,
                 charged: bool = True,
                 right: bool = True) -> None:
        self.bullet_spawner: SpawnerClassicBullet = SpawnerClassicBullet(bullet_image_path, bullet_sizes,
                                                                         bullet_enemy_name, bullet_damage,
                                                                         bullet_life_time, bullet_physical)
        self.bullets: int = bullets
        self.equiped: bool = equiped
        self.charged: bool = charged
        self.right: bool = right
        self.timer_charge: Timer = Timer()
        self.time_charge: float = time_charge
    
    def recharge(self) -> None:
        if not self.charged:
            self.recharge_options()
    
    def recharge_options(self) -> None:
        time: float = self.timer_charge.get_time()
        if time >= self.time_charge:
            self.charged = True
            self.timer_charge.restart()
    
    def shoot(self, owner_pos: tuple[float, float],
              owner_sizes: tuple[float, float], collection) -> None:
        if self.equiped and (self.bullets > 0):
            self.shoot_options(owner_pos, owner_sizes, collection)
    
    def shoot_options(self, owner_pos: tuple[float, float],
                      owner_sizes: tuple[float, float], collection) -> None:
        """Preferable collection is BulletsList"""
        if self.charged:
            bullet_pos: tuple[float, float] = self.get_bullet_pos(owner_pos, owner_sizes)
            bullet = self.bullet_spawner.spawn(bullet_pos)
            bullet.right = self.right
            bullet.activated = True
            self.bullets -= 1
            collection.append(bullet)
            self.charged = False
    
    def get_bullet_pos(self, owner_pos: tuple[float, float],
                       owner_sizes: tuple[float, float]) -> tuple[float, float]:
        if self.right:
            x: float = owner_pos[0]
        else:
            x: float = owner_pos[0] - owner_sizes[0] * .1 - self.bullet_spawner.sizes[0]
        y: float = owner_pos[1]
        return x, y
    
    def __del__(self) -> None:
        pass


class ParabolaGun(ClassicGun):
        def __init__(self, bullet_image_path: str,
                 bullet_sizes: tuple[float, float],
                 bullet_fly_angle: float,
                 bullets: int = 10,
                 time_charge: int = 1,
                 bullet_damage: int = 1,
                 bullet_enemy_name: int = 0,
                 bullet_life_time: float = 8,
                 bullet_physical: bool = True,
                 equiped: bool = True,
                 charged: bool = True,
                 right: bool = True,
                 down: bool = True) -> None:
            super().__init__(bullet_image_path, bullet_sizes, bullets, time_charge, bullet_damage,
                             bullet_enemy_name, bullet_life_time, bullet_physical, equiped, charged, right)
            self.bullet_spawner: SpawnerParabolaBullet = SpawnerParabolaBullet(bullet_image_path,
                                                                               bullet_sizes,
                                                                               bullet_fly_angle,
                                                                               bullet_enemy_name,
                                                                               bullet_damage, 
                                                                               bullet_life_time,
                                                                               bullet_physical,
                                                                               right,
                                                                               down)
            self.down: bool = down
        
        def shoot_options(self, owner_pos: tuple[float, float],
                      owner_sizes: tuple[float, float], collection) -> None:
            """Preferable collection is BulletsList"""
            if self.charged:
                bullet_pos: tuple[float, float] = self.get_bullet_pos(owner_pos, owner_sizes)
                bullet = self.bullet_spawner.spawn(bullet_pos)
                bullet.parabola_motion.down = self.down
                bullet.right = self.right
                bullet.activated = True
                collection.append(bullet)
                self.bullets -= 1
                self.charged = False
        
        def __del__(self) -> None:
            pass
    