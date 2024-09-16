from engine.block import LifeShroom, SuperShroom, MarioBlock, Coin, FireFlower, Rain
from engine.platforms import CircleMovePlatform, RotatingPlatform, BoatPlatform, LiftPlatform
from engine.platforms import ParabolaPlatform
from engine.bullet import Bullet, ClassicBullet, ParabolaBullet
from engine.constants import Sizes, DrawBounds
from engine.interfaces import Spawner
from math import pi
import pygame as pg


SIZE: float = Sizes().size


class SpawnerBullet(Spawner):
    """Entity name is taken from the EntityName enumeration"""
    def __init__(self, image_path: str,
                 sizes: tuple[float, float],
                 damage: int = 1,
                 enemy_name: int = 0,
                 life_time: float = 5,
                 physical: bool = True) -> None:
        super().__init__()
        self._image = pg.image.load(image_path).convert()
        self._sizes: tuple[float, float] = sizes
        self._damage: int = damage
        self._enemy_name: int = enemy_name
        self._life_time: float = life_time
        self._physical: bool = physical
    
    def spawn(self, pos: tuple[float, float]) -> Bullet:
        return Bullet(self._image, self._sizes, pos, self._enemy_name,
                      self._damage, self._life_time, phys=self._physical)
    
    @property
    def sizes(self) -> tuple[float, float]:
        return self._sizes
    
    def __del__(self) -> None:
        pass


class SpawnerClassicBullet(SpawnerBullet):
    def __init__(self, image_path: str,
                 sizes: tuple[float, float],
                 enemy_name: int = 0,
                 damage: int = 1,
                 life_time: float = 8,
                 physical: bool = True) -> None:
        super().__init__(image_path, sizes, damage, enemy_name, life_time, physical)
        self._speed: float = SIZE * .8
    
    def spawn(self, pos: tuple[float, float]) -> ClassicBullet:
        return ClassicBullet(self._image, self._sizes, pos, self._speed, self._speed,
                             self._enemy_name, self._damage, self._life_time, phys=self._physical)
    
    def __del__(self) -> None:
        pass


class SpawnerParabolaBullet(SpawnerClassicBullet):
    """Give argument fly_angle in degrees"""
    def __init__(self, image_path: str,
                 sizes: tuple[float, float],
                 fly_angle: float,
                 enemy_name: int = 0,
                 damage: int = 1,
                 life_time: float = 8,
                 physical: bool = True,
                 right: bool = True,
                 down: bool = True) -> None:
        super().__init__(image_path, sizes, enemy_name, damage, life_time, physical)
        self._fly_angle: float = fly_angle
        self._right: bool = right
        self._down: bool = down
    
    def spawn(self, pos: tuple[float, float]) -> ParabolaBullet:
        return ParabolaBullet(self._image, self._sizes, pos, self._speed, self._speed, self._fly_angle,
                              self._life_time, self._enemy_name, self._damage, right=self._right,
                              down=self._down, phys=self._physical)
    
    def __del__(self) -> None:
        pass


class SpawnerRain(Spawner):
    def __init__(self, image_path: str, 
                 drips_quantity: int = 200) -> None:
        drw: DrawBounds = DrawBounds()
        self.__bounds_y: tuple[float, float] = drw.bound_y[0], drw.bound_y[1]
        self.__bounds_x: tuple[float, float] = drw.bound_x
        self.__sizes: tuple[float, float] = SIZE * .125, SIZE * .25
        self.__quantity: int = drips_quantity
        self.__speed: float = SIZE
        self.image = pg.image.load(image_path).convert()
    
    def spawn(self) -> Rain:
        return Rain(self.image, self.__speed, self.__speed, self.__bounds_y[1],
                    self.__bounds_x, self.__bounds_y, self.__sizes, self.__quantity)
    
    def __del__(self) -> None:
        pass


class SpawnerLifeShroom(Spawner):
    def __init__(self) -> None:
        shroom_path: str = 'Assets/Sprites/Items/Monos/LifeShroom.bmp'
        sound_path: str = 'Assets/Music/extra_health.ogg'
        self.__shroom_image = pg.image.load(shroom_path).convert()
        self.__shroom_sizes: tuple[float, float] = SIZE, SIZE
        self.__shroom_speed: tuple[float, float] = SIZE * .05
        self.__shroom_mass: float = SIZE * .2
        self.__sound = pg.mixer.Sound(sound_path)
    
    def spawn(self, pos: tuple[float, float]) -> LifeShroom:
        return LifeShroom(self.__shroom_image, self.__sound, SIZE * .15,
                          self.__shroom_sizes, self.__shroom_speed, self.__shroom_mass, pos)

    @property
    def sizes(self) -> tuple[float, float]:
        return self.__shroom_sizes
    
    def __del__(self) -> None:
        pass


class SpawnerSuperShroom(Spawner):
    def __init__(self) -> None:
        shroom_path: str = 'Assets/Sprites/Items/Monos/SuperShroom.bmp'
        sound_path: str = 'Assets/Music/bonus.ogg'
        self.__shroom_image = pg.image.load(shroom_path).convert()
        self.__shroom_sizes: tuple[float, float] = SIZE, SIZE
        self.__shroom_speed: tuple[float, float] = SIZE * .05
        self.__shroom_mass: float = SIZE * .2
        self.__sound = pg.mixer.Sound(sound_path)

    def spawn(self, pos: tuple[float, float]) -> SuperShroom:
        return SuperShroom(self.__shroom_image, self.__sound, SIZE * .15,
                           self.__shroom_sizes, self.__shroom_speed, self.__shroom_mass, pos)

    @property
    def sizes(self) -> tuple[float, float]:
        return self.__shroom_sizes

    def __del__(self) -> None:
        pass
       

class SpawnerMarioBlock(Spawner):
    def __init__(self) -> None:
        self.__block_sizes: tuple[float, float] = SIZE, SIZE
        block_path: str = 'Assets/Sprites/Blocks/Monos/Bricks.bmp'
        self.block_img = pg.image.load(block_path).convert()
        brick_snd_path: str = 'Assets/Music/brick.ogg'
        self.__brick_sound = pg.mixer.Sound(brick_snd_path)
        break_snd_path: str = 'Assets/Music/breakblock.ogg'
        self.__break_sound = pg.mixer.Sound(break_snd_path)
    
    def spawn(self, pos: tuple[float, float]) -> MarioBlock:
        return MarioBlock(self.block_img, self.__brick_sound, self.__break_sound, self.__block_sizes, pos)

    @property
    def sizes(self) -> tuple[float, float]:
        return self.__block_sizes

    def __del__(self) -> None:
        pass


class SpawnerPlatform(Spawner):
    def __init__(self) -> None:
        img_path: str = 'Assets/Sprites/Blocks/Monos/Platform.bmp'
        brick_snd_path: str = 'Assets/Music/brick.ogg'
        break_snd_path: str = 'Assets/Music/breakblock.ogg'
        self._sizes: tuple[float, float] = SIZE * 3, SIZE
        self._image = pg.image.load(img_path).convert()
        self._brick_sound = pg.mixer.Sound(brick_snd_path)
        self._break_sound = pg.mixer.Sound(break_snd_path)

    def spawn(self, pos: tuple[float, float]) -> MarioBlock:
        return MarioBlock(self._image, self._brick_sound, self._break_sound, self._sizes, pos, destructible=False, phys=False)

    @property
    def sizes(self) -> tuple[float, float]:
        return self._sizes

    def __del__(self) -> None:
        pass


class SpawnerParabolaPlatform(SpawnerPlatform):
    """Give argument fly_angle in degrees"""
    def __init__(self, fly_angle: float, right: bool = True, down: bool = True) -> None:
        super().__init__()
        self._speed: float = SIZE * .15
        self._max_speed: float = SIZE * .6
        self._fly_angle: float = fly_angle
        self._right: bool = right
        self._down: bool = down
    
    def spawn(self, pos: tuple[float, float]) -> ParabolaPlatform:
        return ParabolaPlatform(self._image, self._brick_sound, self._break_sound,
                                self._speed, self._max_speed, self._fly_angle, self._sizes, pos,
                                right=self._right, down=self._down)
    
    @property
    def sizes(self) -> tuple[float, float]:
        return self._sizes
    
    def __del__(self) -> None:
        pass


class SpawnerBoatPlatform(SpawnerPlatform):
    """Length is the length of movement"""
    def __init__(self, length: float) -> None:
        super().__init__()
        self._speed: float = SIZE * .05
        self._max_speed: float = SIZE * .2
        self._length = length

    def spawn(self, pos: tuple[float, float]) -> BoatPlatform:
        return BoatPlatform(self._image, self._brick_sound, self._break_sound,
                             self._speed, self._length, self._max_speed, self._sizes, pos)

    def __del__(self) -> None:
        pass


class SpawnerLiftPlatform(SpawnerBoatPlatform):
    """Length is the length of movement"""
    def __init__(self, length: float) -> None:
        super().__init__(length)

    def spawn(self, pos: tuple[float, float]) -> LiftPlatform:
        return LiftPlatform(self._image, self._brick_sound, self._break_sound,
                            self._speed, self._length, self._max_speed, self._sizes, pos)

    def __del__(self) -> None:
        pass


class SpawnerCircleMovePlatform(SpawnerPlatform):
    def __init__(self, circle_radius: float,
                 clockwise: bool = True) -> None:
        super().__init__()
        self._clockwise: bool = clockwise
        self._radius: float = circle_radius
        self._speed: float = pi / 32

    def spawn(self, pos: tuple[float, float]) -> CircleMovePlatform:
        return CircleMovePlatform(self._image, self._brick_sound, self._break_sound, self._speed,
                                  self._speed, self._radius, pos, self._sizes, pos, clockwise=self._clockwise)

    def __del__(self) -> None:
        pass


class SpawnerRotatingPlatform(SpawnerPlatform):
    def __init__(self, right: bool = True) -> None:
        super().__init__()
        self._right: bool = right

    def spawn(self, pos: tuple[float, float]) -> RotatingPlatform:
        return RotatingPlatform(self._image, self._brick_sound, self._break_sound, self._sizes, pos, right=self._right)

    def __del__(self) -> None:
        pass
    

class SpawnerCoin(Spawner):
    def __init__(self) -> None:
        self.__coin_sizes: tuple[float, float] = SIZE, SIZE
        com_path: str = 'Assets/Sprites/Items/Polys/Coin/'
        self.__coin_imgs = []
        for i in range(3):
            path: str = f'{com_path}{i}.bmp'
            image = pg.image.load(path).convert()
            self.__coin_imgs.append(image)
        coin_snd_path: str = 'Assets/Music/coin.ogg'
        self.__sound = pg.mixer.Sound(coin_snd_path)

    def spawn(self, pos: tuple[float, float]) -> Coin:
        return Coin(self.__coin_imgs, self.__sound, self.__coin_sizes, pos)

    @property
    def sizes(self) -> tuple[float, float]:
        return self.__coin_sizes

    def __del__(self) -> None:
        pass


class SpawnerFireFlower(Spawner):
    def __init__(self) -> None:
        self.__sizes: tuple[float, float] = SIZE, SIZE
        com_path: str = 'Assets/Sprites/Items/Polys/FireFlower/'
        self.__images = []
        for i in range(4):
            path: str = f'{com_path}{i}.bmp'
            image = pg.image.load(path).convert()
            self.__images.append(image)
        sound_path: str = 'Assets/Music/bonus.ogg'
        self.__sound = pg.mixer.Sound(sound_path)

    def spawn(self, pos: tuple[float, float]) -> FireFlower:
        return FireFlower(self.__images, self.__sound, self.__sizes, pos)

    @property
    def sizes(self) -> tuple[float, float]:
        return self.__sizes

    def __del__(self) -> None:
        pass
