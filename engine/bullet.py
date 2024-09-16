from engine.motions import Parabola
from engine.interfaces import Interactive
from engine.component import Speed
from engine.block import MonoBlock
from engine.tools import Timer


class Bullet(MonoBlock, Interactive):
    """Entity name is taken from the EntityName enumeration"""
    def __init__(self, image,
                 sizes: tuple[float, float],
                 pos: tuple[float, float],
                 enemy_name: int = 0,
                 damage: int = 1,
                 life_time: float = 5,
                 destructible: bool = True,
                 in_activity: bool = True,
                 destroyed: bool = False,
                 activated: bool = False,
                 on_screen: bool = True,
                 static: bool = False,
                 right: bool = True,
                 phys: bool = True) -> None:
        MonoBlock.__init__(self, image, sizes, pos, destructible, in_activity, 
                           destroyed, on_screen, static, right, phys)
        self.life_timer: Timer = Timer()
        self.enemy_name: int = enemy_name
        self.damage: int = damage
        self.life_time: float = life_time
        self.activated: bool = activated
    
    def draw(self, wnd) -> None:
        if self.activated:
            super().draw(wnd)
    
    def init_update(self) -> tuple[float, float]:
        self.control_bullet_life()
        pos: tuple[float, float] = super().init_update()
        return pos
    
    def control_bullet_life(self) -> None:
        if self.activated and not self.destroyed:
            self.destroy_bullet()
    
    def destroy_bullet(self) -> None:
        time: float = self.life_timer.get_time()
        if time >= self.life_time:
            self.destroyed = True
    
    def interact(self, target) -> None:
        if self.rect.colliderect(target.rect):
            self.interact_options(target)
    
    def interact_options(self, target) -> None:
        if self.activated and not self.destroyed:
            self.kill_target(target)
    
    def kill_target(self, target) -> None:
        if target.name == self.enemy_name:
            self.kill_options(target)
    
    def kill_options(self, target) -> None:
        if hasattr(target, 'superform') and target.superform:
            return
        elif hasattr(target, 'big') and target.big:
            target.big = False
        elif hasattr(target, 'fireform') and target.fireform:
            target.fireform = False
        elif hasattr(target, 'hp'):
            target.hp.decrease_health(self.damage)
        else:
            target.alive = False
        self.life_timer.restart()
        self.destroyed = True
        self.static = True
    
    def __del__(self) -> None:
        pass


class ClassicBullet(Bullet):
    def __init__(self, image,
                 sizes: tuple[float, float],
                 pos: tuple[float, float],
                 speed: float,
                 max_speed: float,
                 enemy_name: int = 0,
                 damage: int = 1,
                 life_time: float = 8,
                 destructible: bool = True,
                 in_activity: bool = True,
                 destroyed: bool = False,
                 activated: bool = False,
                 on_screen: bool = True,
                 is_move: bool = True,
                 static: bool = False,
                 right: bool = True,
                 phys: bool = True) -> None:
        super().__init__(image, sizes, pos, enemy_name, damage, life_time, destructible,
                         in_activity, destroyed, activated, on_screen, static, right, phys)
        self.speed: Speed = Speed(speed, max_speed, right)
        self.is_move: bool = is_move
    
    def main_update(self, pos: tuple[float, float]) -> None:
        self.motion_x()
        super().main_update(pos)
    
    def motion_x(self) -> None:
        if self.is_move and self.activated:
            self.speed.move_x(self.rect, self.right)
    
    def __del__(self) -> None:
        pass


class ParabolaBullet(Bullet):
    """Give argument fly_angle in degrees"""
    def __init__(self, image,
                 sizes: tuple[float, float],
                 pos: tuple[float, float],
                 speed: float,
                 max_speed: float,
                 fly_angle: float,
                 life_time: float = 8,
                 enemy_name: int = 0,
                 damage: int = 1,
                 destructible: bool = True,
                 in_activity: bool = True,
                 destroyed: bool = False,
                 activated: bool = False,
                 on_screen: bool = True,
                 is_move: bool = True,
                 static: bool = False,
                 right: bool = True,
                 down: bool = True,
                 phys: bool = True) -> None:
        super().__init__(image, sizes, pos, enemy_name, damage, life_time, destructible,
                         in_activity, destroyed, activated, on_screen, static, right, phys)
        self.parabola_motion: Parabola = Parabola(speed, max_speed, fly_angle, right, down)
        self.is_move: bool = is_move
    
    def main_update(self, pos: tuple[float, float]) -> None:
        super().main_update(pos)
        self.motion()
    
    def sync_right(self) -> None:
        super().sync_right()
        self.parabola_motion.right = self.right
    
    def motion(self) -> None:
        if self.activated and self.is_move:
            self.parabola_motion.move_rect(self.rect, special=True)
    
    def __del__(self) -> None:
        pass
