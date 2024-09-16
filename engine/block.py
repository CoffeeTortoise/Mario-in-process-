from engine.component import Updatable, Speed, Gravity
from engine.interfaces import Interactive, GhostSprite
from engine.picture import Sprite, AnimatedSprite
from engine.tools import Soundman, RandPos
from engine.enumerations import EntityName
from engine.shapes import RectangleShape
from engine.constants import Sizes
from engine.motions import Drip
from engine.tools import Timer
from time import sleep
import pygame as pg


class Lightning(GhostSprite):
    def __init__(self, image,
                 thunder_sound,
                 time_period: float,
                 light_width: float,
                 bounds_x: tuple[float, float],
                 alpha: int = 200,
                 static: bool = True,
                 color: tuple[int, ...] = (255, 255, 255)) -> None:
        size: Sizes = Sizes()
        self.surface: pg.surface.Surface = pg.surface.Surface(size.wnd_size)
        self.bleach: RectangleShape = RectangleShape((0, 0), size.wnd_size, color)
        self.sound: pg.mixer.Sound = thunder_sound
        self.__timer: Timer = Timer()
        self.surface.set_alpha(alpha)
        image.set_colorkey((255, 255, 255))
        self.image: pg.surface.Surface = pg.transform.scale(image, (light_width, size.wnd_size[1]))
        self.rect = self.image.get_rect()
        self.rect.width, self.rect.height = light_width, size.wnd_size[1]
        self.rect.left, self.rect.top = 0, 0
        self.time_period: float = time_period
        self.time_thunder: float = self.time_period + 1
        self.time_ending: float = self.time_thunder + .3
        self.bounds_x: tuple[float, float] = bounds_x
        self._name: int = EntityName.other
        self.light: bool = False
        self.thunder: bool = False
        self.static: bool = static
    
    def draw(self, wnd) -> None:
        if self.light:
            wnd.blit(self.image, self.rect)
        if self.thunder:
            self.bleach.draw(self.surface)
            wnd.blit(self.surface, (0, 0))
            sleep(1)
    
    def update(self) -> None:
        time: float = self.__timer.get_time()
        if (time >= self.time_period) and (time <= self.time_thunder):
            self.generate_light_pos()
            self.thunder = False
        if (time > self.time_thunder) and (time <= self.time_ending):
            self.thunder = True
            self.light = False
        if (time > self.time_ending):
            self.sound.play()
            self.thunder = False
            self.__timer.restart()
    
    def generate_light_pos(self) -> None:
        if not self.light:
            light_x: float = RandPos.rand_num(self.bounds_x[0], self.bounds_x[1])
            self.rect.left = light_x
            self.light = True
    
    def shift(self, dx: float = 0, dy: float = 0) -> None:
        if not self.static:
            x1: float = self.bounds_x[0] + dx
            x2: float = self.bounds_x[1] + dx
            bounds_x: tuple[float, float] = x1, x2
            self.set_bounds_x(bounds_x)
    
    def set_bounds_x(self, bounds_x) -> None:
        if bounds_x != self.bounds_x:
            self.bounds_x = bounds_x
    
    def resize(self, sizes: tuple[float, float]) -> None:
        """Changes the sizes of the lightning"""
        light_sizes: tuple[float, float] = self.rect.width, self.rect.height
        if light_sizes != sizes:
            self.resize_options(sizes)
    
    def resize_options(self, sizes: tuple[float, float]) -> None:
        """Changes the sizes of the lightning without checking current sizes"""
        self.image = pg.transform.scale(self.image, sizes)
        self.rect.width, self.rect.height = sizes
    
    @property
    def pos(self) -> tuple[float, float]:
        """Positions of the lightning"""
        return self.rect.left, self.rect.top
    
    @property
    def sizes(self) -> tuple[float, float]:
        """Sizes of the lightning"""
        return self.rect.width, self.rect.height
    
    @property
    def name(self) -> int:
        return self._name
    
    def __del__(self) -> None:
        pass


class Clouds:
    def __init__(self, image,
                 speed: float,
                 max_speed: float,
                 bounds_x: tuple[float, float],
                 bounds_y: tuple[float, float],
                 sizes: tuple[float, float],
                 quantity: int = 6,
                 to_right: bool = True,
                 stop_clouds: bool = False) -> None:
        self.__cloud = []
        for _ in range(quantity):
            pos: tuple[float, float] = RandPos.rand_pos(bounds_x, bounds_y)
            ma_speed: Speed = Speed(speed, max_speed, to_right)
            cloud: Sprite = Sprite(image, sizes, pos, static=True)
            self.__cloud.append([cloud, ma_speed])
        self.bounds_x: tuple[float, float] = bounds_x
        self._name: int = EntityName.other
        self.stop_clouds: bool = stop_clouds
        self.right: bool = to_right
        
    def draw(self, wnd) -> None:
        for cloud in self.__cloud:
            cloud[0].draw(wnd)
        
    def update(self) -> None:
        for cloud in self.__cloud:
            if not self.stop_clouds:
                self.cloud_move(cloud)
        
    def cloud_move(self, cloud) -> None:
        cloud[1].move_x(cloud[0].rect, to_right=self.right)
        out: bool = self.cloud_out(cloud)
        if out:
            self.recover_cloud_pos(cloud[0])
    
    def recover_cloud_pos(self, cloud) -> None:
        if self.right:
            cloud.rect.left = self.bounds_x[0]
        else:
            cloud.rect.left = self.bounds_x[1]
        
    def cloud_out(self, cloud) -> bool:
        if (cloud[0].pos[0] >= self.bounds_x[1]) and self.right:
            return True
        elif (cloud[0].pos[0] <= self.bounds_x[0]) and not self.right:
            return True
        else:
            return False
    
    def shift(self, dx: float = 0, dy: float = 0) -> None:
        pass
    
    @property
    def name(self) -> int:
        return self._name
    
    def __del__(self) -> None:
        pass


class Rain:
    def __init__(self, image,
                 speed: float,
                 max_speed: float,
                 middle_line: float,
                 bounds_x: tuple[float, float],
                 bounds_y: tuple[float, float],
                 sizes: tuple[float, float],
                 quantity: int = 100,
                 rain_on: bool = True) -> None:
        self.__rain: list = []
        for _ in range(quantity):
            drip: Sprite = Sprite(image, sizes, (0, 0), static=True)
            drip_motion: Drip = Drip(speed, max_speed, middle_line, bounds_x, bounds_y)
            self.__rain.append([drip, drip_motion])
        self.rain_on: bool = rain_on
        self._name: int = EntityName.other
    
    def draw(self, wnd) -> None:
        for drip in self.__rain:
            drip[0].draw(wnd)
    
    def update(self) -> None:
        for drip in self.__rain:
            drip[0].update()
            if self.rain_on:
                drip[1].move_rect(drip[0].rect)
    
    def shift(self, dx: float = 0, dy: float = 0) -> None:
        pass
    
    @property
    def name(self) -> int:
        return self._name
    
    def __del__(self) -> None:
        pass
        
        
class MonoBlock(Sprite):
    """phys is responsible for handling collisions with other objects if an instance of the 
    class is in InteractiveSprites collection."""
    def __init__(self, image,
                 sizes: tuple[float, float],
                 pos: tuple[float, float],
                 destructible: bool = True,
                 in_activity: bool = True,
                 destroyed: bool = False,
                 on_screen: bool = True,
                 static: bool = False,
                 right: bool = True,
                 phys: bool = True) -> None:
        super().__init__(image, sizes, pos, on_screen, static, right)
        self.updatable: Updatable = Updatable(in_bound=in_activity)
        self.destructible: bool = destructible
        self.destroyed: bool = destroyed
        self.physical: bool = phys
    
    def draw(self, wnd) -> None:
        if not self.destroyed:
            super().draw(wnd)
    
    def shift(self, dx: float = 0, dy: float = 0) -> None:
        if not self.destroyed:
            super().shift(dx, dy)
    
    def update(self) -> None:
        pos: tuple[float, float] = self.init_update()
        if self.updatable.in_bound and not self.destroyed:
            self.main_update(pos)
    
    def init_update(self) -> tuple[float, float]:
        pos: tuple[float, float] = self.rect.left, self.rect.top
        self.updatable.check_bound(pos)
        self.fix_destruction()
        return pos
    
    def main_update(self, pos: tuple[float, float]) -> None:
        self.drawable.check_bound(pos)
        self.sync_right()
        self.change_image()
    
    def fix_destruction(self) -> None:
        if not self.destructible:
            self.destroyed = False
        if self.destroyed:
            self.static = True
    
    def __del__(self) -> None:
        pass


class MarioBlock(MonoBlock, Interactive):
    """Usual block from Mario85"""
    def __init__(self, image,
                 brick_sound,
                 breakblock_sound,
                 sizes: tuple[float, float],
                 pos: tuple[float, float],
                 destructible: bool = True,
                 in_activity: bool = True,
                 destroyed: bool = False,
                 on_screen: bool = True,
                 static: bool = False,
                 right: bool = True,
                 phys: bool = True) -> None:
        MonoBlock.__init__(self, image, sizes, pos, destructible, in_activity,
                           destroyed, on_screen, static, right, phys)
        self.sound_broken: Soundman = Soundman(breakblock_sound)
        self.sound_clsn = brick_sound
    
    def interact(self, target) -> None:
        check_active: bool = target.rect.colliderect(self.rect) and self.updatable.in_bound
        if check_active and not self.destroyed:
            self.interact_options(target)
    
    def interact_options(self, target) -> None:
        if (hasattr(target, 'big') and target.big) and self.destructible:
            self.sound_broken.play()
            self.destroyed = True
        else:
            self.sound_clsn.play()
    
    def __del__(self) -> None:
        pass
       

class RunningBlock(MonoBlock):
    def __init__(self, image,
                 max_speed: float,
                 sizes: tuple[float, float],
                 speed: float,
                 pos: tuple[float, float],
                 destructible: bool = True,
                 in_activity: bool = True,
                 destroyed: bool = False,
                 on_screen: bool = True,
                 static: bool = False,
                 is_move: bool = True,
                 right: bool = True,
                 phys: bool = True) -> None:
        super().__init__(image, sizes, pos, destructible, in_activity,
                         destroyed, on_screen, static, right, phys)
        self.speed: Speed = Speed(speed, max_speed, right)
        self.to_right: bool = right
        self.is_move: bool = is_move
    
    def update(self) -> None:
        pos: tuple[float, float] = self.init_update()
        if self.updatable.in_bound and not self.destroyed:
            self.main_update(pos)
    
    def main_update(self, pos: tuple[float, float]) -> None:
        if self.is_move:
            self.speed.move_x(self.rect, self.to_right)
        super().main_update(pos)
    
    def sync_right(self) -> None:
        self.right = self.speed.right
        super().sync_right()
    
    def fix_destruction(self) -> None:
        super().fix_destruction()
        if self.destroyed:
            self.is_move = False
    
    def __del__(self) -> None:
        pass

class Box(RunningBlock):
    """Basically RunningBlock with a gravity"""
    def __init__(self, image,
                 max_speed: float,
                 sizes: tuple[float, float],
                 speed: float,
                 mass: float,
                 pos: tuple[float, float],
                 destructible: bool = True,
                 in_activity: bool = True,
                 destroyed: bool = False,
                 on_screen: bool = True,
                 grounded: bool = False,
                 static: bool = False,
                 is_move: bool = True,
                 right: bool = True,
                 phys: bool = True) -> None:
        super().__init__(image, max_speed, sizes, speed, pos, destructible,
                         in_activity, destroyed, on_screen, static, is_move, right, phys)
        self.gravity: Gravity = Gravity(mass, sizes[1] * .5, grounded, controlled=True)
    
    def main_update(self, pos: tuple[float, float]) -> None:
        self.gravity.apply_gravity(self.rect)
        super().main_update(pos)
    
    def fix_destruction(self) -> None:
        if not self.destructible:
            self.destroyed = False
        if self.destroyed:
            self.static = True
            self.is_move = False
            self.gravity.grounded = True
    
    def __del__(self) -> None:
        pass


class LifeShroom(Box, Interactive):
    def __init__(self, image,
                 sound,
                 max_speed: float,
                 sizes: tuple[float, float],
                 speed: float,
                 mass: float,
                 pos: tuple[float, float],
                 destructible: bool = True,
                 in_activity: bool = True,
                 destroyed: bool = False,
                 on_screen: bool = True,
                 grounded: bool = False,
                 static: bool = False,
                 is_move: bool = True,
                 right: bool = True,
                 phys: bool = True,
                 lives: int = 1) -> None:
        Box.__init__(self, image, max_speed, sizes, speed, mass, pos, destructible, 
                     in_activity, destroyed, on_screen, grounded, static, is_move, right, phys)
        self.sound: Soundman = Soundman(sound)
        self.lives: int = lives
    
    def interact(self, target) -> None:
        check_active: bool = target.rect.colliderect(self.rect) and self.updatable.in_bound
        if check_active and not self.destroyed:
            self.interact_options(target)
    
    def interact_options(self, target) -> None:
        target.lives += self.lives
        self.destroyed = True
        self.sound.play()
    
    def __del__(self) -> None:
        pass


class SuperShroom(LifeShroom):
    def __init__(self, image,
             sound,
             max_speed: float,
             sizes: tuple[float, float],
             speed: float,
             mass: float,
             pos: tuple[float, float],
             destructible: bool = True,
             in_activity: bool = True,
             destroyed: bool = False,
             on_screen: bool = True,
             grounded: bool = False,
             static: bool = False,
             is_move: bool = True,
             right: bool = True,
             phys: bool = True,
             alive: bool | int = True) -> None:
        super().__init__(image, sound, max_speed, sizes, speed, mass, pos, destructible, in_activity,
                          destroyed, on_screen, grounded, static, is_move, right, phys, alive)

    def interact_options(self, target) -> None:
        if not target.big:
            target_sizes: tuple[float, float] = target.sizes[0] * 2, target.sizes[1] * 2
            target.total_resize(target_sizes)
            target.big = self.lives
            self.destroyed = True
            self.sound.play()

    def __del__(self) -> None:
        pass
        

class PolyBlock(AnimatedSprite):
    """phys is responsible for handling collisions with other objects if an instance of the 
    class is in InteractiveSprites collection."""
    def __init__(self, images,
             sizes: tuple[float, float],
             pos: tuple[float, float],
             frame_time: float = .15,
             destructible: bool = True,
             in_activity: bool = True,
             destroyed: bool = False,
             play_anime: bool = True,
             on_screen: bool = True,
             static: bool = False,
             right: bool = True,
             phys: bool = True) -> None:
        super().__init__(images, sizes, pos, frame_time, play_anime, on_screen, static, right)
        self.updatable: Updatable = Updatable(in_bound=in_activity)
        self.destructible: bool = destructible
        self.destroyed: bool = destroyed
        self.physical: bool = phys
        
    def draw(self, wnd) -> None:
        if not self.destroyed:
            super().draw(wnd)
    
    def shift(self, dx: float = 0, dy: float = 0) -> None:
        if not self.destroyed:
            super().shift(dx, dy)
    
    def update(self) -> None:
        pos: tuple[float, float] = self.init_update()
        if self.updatable.in_bound and not self.destroyed:
            self.main_update(pos)
    
    def init_update(self) -> tuple[float, float]:
        pos: tuple[float, float] = self.rect.left, self.rect.top
        self.updatable.check_bound(pos)
        self.fix_destruction()
        return pos
    
    def main_update(self, pos: tuple[float, float]) -> None:
        self.drawable.check_bound(pos)
        self.sync_right()
        self.change_image()
    
    def fix_destruction(self) -> None:
        if not self.destructible:
            self.destroyed = False
        if self.destroyed:
            self.static = True
    
    def __del__(self) -> None:
        pass


class Coin(PolyBlock, Interactive):
    def __init__(self, images, sound,
             sizes: tuple[float, float],
             pos: tuple[float, float],
             frame_time: float = .15,
             value: int = 1,
             destructible: bool = True,
             in_activity: bool = True,
             destroyed: bool = False,
             play_anime: bool = True,
             on_screen: bool = True,
             static: bool = False,
             right: bool = True,
             phys: bool = False) -> None:
        PolyBlock.__init__(self, images, sizes, pos, frame_time, destructible, in_activity,
                            destroyed, play_anime, on_screen, static, right, phys)
        self.sound: Soundman = Soundman(sound)
        self.value: int = value
        
    def interact(self, target) -> None:
        check_active: bool = target.rect.colliderect(self.rect) and self.updatable.in_bound
        if check_active and not self.destroyed:
            self.interact_options(target)
    
    def interact_options(self, target) -> None:
        target.coins += self.value
        self.destroyed = True
        self.sound.play()

    def __del__(self) -> None:
        pass


class FireFlower(PolyBlock, Interactive):
    def __init__(self, images, sound,
             sizes: tuple[float, float],
             pos: tuple[float, float],
             frame_time: float = .15,
             destructible: bool = True,
             in_activity: bool = True,
             destroyed: bool = False,
             play_anime: bool = True,
             on_screen: bool = True,
             static: bool = False,
             right: bool = True,
             phys: bool = False,  
             fire: bool = True) -> None:
        PolyBlock.__init__(self, images, sizes, pos, frame_time, destructible, in_activity,
                            destroyed, play_anime, on_screen, static, right, phys)
        self.sound: Soundman = Soundman(sound)
        self.fire: bool = fire
        
    def interact(self, target) -> None:
        check_active: bool = target.rect.colliderect(self.rect) and self.updatable.in_bound
        if check_active and not self.destroyed:
            self.interact_options(target)
    
    def interact_options(self, target) -> None:
        if not target.fireform:
            target.fireform = self.fire
            target.firegun.bullets = 10
        else:
            target.firegun.bullets += 10
        self.destroyed = True
        self.sound.play()

    def __del__(self) -> None:
        pass
