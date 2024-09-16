from engine.component import Speed, Gravity, Jump
from engine.picture import AnimatedSprite, Skin
from engine.enumerations import EntityName
from engine.charguns import SpawnerFiregun
from engine.bar import CounterItems
from engine.constants import Sizes
from time import sleep
import pygame as pg


class Model0(AnimatedSprite):
    """An animated sprite, augmented with a motion component along the X-axis. Based on the 
    AnimatedSprite class."""
    def __init__(self, images,
                 sizes: tuple[float, float],
                 pos: tuple[float, float],
                 speed: float,
                 frame_time: float = .15,
                 is_moving: bool = False,
                 play_anime: bool = True,
                 on_screen: bool = True,
                 is_move: bool = True,
                 static: bool = False,
                 right: bool = True) -> None:
        super().__init__(images, sizes, pos, frame_time, play_anime, on_screen, static, right)
        self.speed: Speed = Speed(speed, sizes[0] * .7, right)
        self.is_moving: bool = is_moving
        self.is_move: bool = is_move
    
    def define_image(self) -> None:
        if self.is_moving:
            self.change_image()
        else:
            self.change_image(animate=False)
    
    def sync_right(self) -> None:
        self.right = self.speed.right
        super().sync_right()
    
    def pure_resize(self, sizes: tuple[float, float]) -> None:
        k_speed: float = sizes[0] / self.rect.width
        self.speed.limiter *= k_speed
        super().pure_resize(sizes)
   
    def __del__(self) -> None:
        pass


class Model1(Model0):
    """A playable character. Can move left and right. Based on class Model0"""
    def __init__(self, images,
                 sizes: tuple[float, float],
                 pos: tuple[float, float],
                 speed: float,
                 frame_time: float = .15,
                 is_moving: bool = False,
                 play_anime: bool = True,
                 on_screen: bool = True,
                 is_move: bool = True,
                 static: bool = False,
                 right: bool = True) -> None:
        super().__init__(images, sizes, pos, speed, frame_time,
                         is_moving, play_anime, on_screen, is_move, static, right)
        self._name: int = EntityName.player
    
    def update(self) -> None:
        pos: tuple[float, float] = self.rect.left, self.rect.top
        self.drawable.check_bound(pos)
        self.motion()
        self.sync_right()
        self.define_image()
    
    def motion(self) -> None:
        keys = pg.key.get_pressed()
        self.motion_x(keys)
    
    def motion_x(self, keys) -> None:
        self.is_moving = False
        self.call_keys_x(keys)
    
    def call_keys_x(self, keys) -> None:
        if self.is_move:
            self.keys_x(keys)
    
    def keys_x(self, keys) -> None:
        if keys[pg.K_LEFT] and keys[pg.K_RIGHT]:
            return
        self.key_left(keys)
        self.key_right(keys)
    
    def key_left(self, keys) -> None:
        if keys[pg.K_LEFT]:
            self.is_moving = True
            self.speed.move_x(self.rect, to_right=False)
    
    def key_right(self, keys) -> None:
        if keys[pg.K_RIGHT]:
            self.is_moving = True
            self.speed.move_x(self.rect)
    
    def __del__(self) -> None:
        pass


class Model2(Model1):
    """Playable character. Augmented with a gravity component"""
    def __init__(self, images,
                 sizes: tuple[float, float],
                 pos: tuple[float, float],
                 speed: float,
                 mass: float,
                 frame_time: float = .15,
                 is_moving: bool = False,
                 play_anime: bool = True,
                 on_screen: bool = True,
                 grounded: bool = False,
                 is_move: bool = True,
                 static: bool = False,
                 right: bool = True) -> None:
        super().__init__(images, sizes, pos, speed, frame_time,
                         is_moving, play_anime, on_screen, is_move, static, right)
        self.gravity: Gravity = Gravity(mass, sizes[1] * .5, grounded)
    
    def update(self) -> None:
        super().update()
        self.gravity.apply_gravity(self.rect)
    
    def __del__(self) -> None:
        pass


class Model3(Model2):
    """Improved to jump"""
    def __init__(self, images,
                 sizes: tuple[float, float],
                 pos: tuple[float, float],
                 ground: float,
                 height: float,
                 speed: float,
                 jump: float,
                 mass: float,
                 frame_time: float = .15,
                 is_moving: bool = False,
                 play_anime: bool = True,
                 on_screen: bool = True,
                 grounded: bool = False,
                 jumpable: bool = True,
                 is_move: bool = True,
                 static: bool = False,
                 jumped: bool = False,
                 right: bool = True) -> None:
        super().__init__(images, sizes, pos, speed, mass, frame_time, 
                         is_moving, play_anime, on_screen, grounded, is_move, static, right)
        self.jump: Jump = Jump(jump, -sizes[1] * .3, ground, height, jumped)
        self.jumpable: bool = jumpable
        self.on_key_jump: bool = False
    
    def shift(self, dx: float = 0, dy: float = 0) -> None:
        super().shift(dx, dy)
        self.jump.ground += dy
    
    def motion(self) -> None:
        keys = pg.key.get_pressed()
        self.motion_x(keys)
        self.motion_up(keys)
    
    def motion_up(self, keys) -> None:
        if self.jumpable:
            self.key_up(keys)
    
    def key_up(self, keys) -> None:
        self.on_key_jump = False
        if keys[pg.K_UP]:
            self.on_key_jump = True
            self.move_up()
        self.fix_jumping()
    
    def fix_jumping(self) -> None:
        if self.jump.in_jumping and not self.on_key_jump:
            self.release_jumping()
    
    def move_up(self) -> None:
        if self.gravity.grounded:
            self.jump.jumping(self.rect)
        if self.jump.jumped:
            self.gravity.grounded = False
    
    def release_jumping(self) -> None:
        self.jump.stop_jumping()
        self.gravity.grounded = False

    def pure_resize(self, sizes: tuple[float, float]) -> None:
        delta_height: float = sizes[1] - self.rect.height
        self.jump.height += delta_height
        super().pure_resize(sizes)
    
    def __del__(self) -> None:
        pass


class Model4(Model3):
    """Improved to interact with the mushrooms of life"""
    def __init__(self, images,
                 sizes: tuple[float, float],
                 pos: tuple[float, float],
                 ground: float,
                 height: float,
                 speed: float,
                 jump: float,
                 mass: float,
                 lives: int = 3,
                 death_sound = None,
                 frame_time: float = .15,
                 is_moving: bool = False,
                 play_anime: bool = True,
                 on_screen: bool = True,
                 grounded: bool = False,
                 jumpable: bool = True,
                 is_move: bool = True,
                 static: bool = False,
                 jumped: bool = False,
                 right: bool = True) -> None:
        super().__init__(images, sizes, pos, ground, height, speed,
                         jump, mass, frame_time, is_moving, play_anime, on_screen,
                         grounded, jumpable, is_move, static, jumped, right)
        sizes: Sizes = Sizes()
        self.__spawn_pos: tuple[float, float] = pos
        self.fnt_size: int = int(sizes.size * .5)
        self.fnt_path: str = 'Assets/SuperMario85.ttf'
        livebar_pos: tuple[float, float] = self.fnt_size, self.fnt_size * .5
        self.live_bar: CounterItems = CounterItems(self.fnt_size, self.fnt_path,
                                                   'Lives: ', pos=livebar_pos, static=True)
        self.lives: int = lives
        self.alive: bool = True if lives else False
        self.death_sound = death_sound
            
    def draw(self, wnd) -> None:
        if self.alive:
            self.draw_options(wnd)

    def draw_options(self, wnd) -> None:
        super().draw(wnd)
        self.live_bar.draw(wnd)
    
    def update(self) -> None:
        self.respawn()
        if self.alive:
            self.update_options()

    def update_options(self) -> None:
        super().update()
        self.live_bar.update()
        self.live_bar.counter.change_text(str(self.lives))
    
    def shift(self, dx: float = 0, dy: float = 0) -> None:
        super().shift(dx, dy)
        self.shift_spawn(dx, dy)
        self.live_bar.shift(dx, dy)

    def respawn(self, pos: tuple[float, float] = (0, 0)) -> None:
        if (self.lives > 0) and not self.alive:
            self.respawn_options(pos)

    def respawn_options(self, pos: tuple[float, float] = (0, 0)) -> None:       
            self.play_death_snd()
            self.set_spawn_pos(pos)
            sleep(2)
            self.lives -= 1
            self.alive = True
            self.rect.left, self.rect.top = self.__spawn_pos

    def play_death_snd(self) -> None:
        if self.death_sound is not None:
            self.death_sound.play()
    
    def shift_spawn(self, dx: float = 0, dy: float = 0) -> None:
        x: float = self.__spawn_pos[0] + dx
        y: float = self.__spawn_pos[1] + dy
        pos: tuple[float, float] = x, y
        self.set_spawn_pos(pos)

    def set_spawn_pos(self, pos: tuple[float, float] = (0, 0)) -> None:
        if (pos != (0, 0)) and (pos != self.__spawn_pos):
            self.__spawn_pos = pos
    
    def __del__(self) -> None:
        pass


class Model5(Model4):
    """Improved to interact with super mushrooms"""
    def __init__(self, images,
                 sizes: tuple[float, float],
                 pos: tuple[float, float],
                 ground: float,
                 height: float,
                 speed: float,
                 jump: float,
                 mass: float,
                 lives: int = 3,
                 death_sound = None,
                 frame_time: float = .15,
                 is_moving: bool = False,
                 play_anime: bool = True,
                 on_screen: bool = True,
                 grounded: bool = False,
                 jumpable: bool = True,
                 is_move: bool = True,
                 static: bool = False,
                 jumped: bool = False,
                 right: bool = True,
                 big: bool = False) -> None:
        super().__init__(images, sizes, pos, ground, height, speed, jump, mass, lives, death_sound, frame_time,
                          is_moving, play_anime, on_screen, grounded, jumpable, is_move, static, jumped, right)
        self.__normal_sizes: tuple[float, float] = sizes
        self.big: bool = big

    def update_options(self) -> None:
        super().update_options()
        self.return_normal_sizes()

    def return_normal_sizes(self) -> None:
        if not self.big:
            self.total_resize(self.__normal_sizes)
        
    def respawn_options(self, pos: tuple[float, float]) -> None:
        self.big = False
        super().respawn_options(pos)

    @property
    def normal_sizes(self) -> tuple[float, float]:
        return self.__normal_sizes

    def __del__(self) -> None:
        pass


class Model6(Model5):
    """Improved to interact with coins"""
    def __init__(self, images,
                 sizes: tuple[float, float],
                 pos: tuple[float, float],
                 ground: float,
                 height: float,
                 speed: float,
                 jump: float,
                 mass: float,
                 coin_limit: int = 10,
                 coins: int = 0,
                 lives: int = 3,
                 death_sound = None,
                 frame_time: float = .15,
                 is_moving: bool = False,
                 play_anime: bool = True,
                 on_screen: bool = True,
                 grounded: bool = False,
                 jumpable: bool = True,
                 is_move: bool = True,
                 static: bool = False,
                 jumped: bool = False,
                 right: bool = True,
                 big: bool = False) -> None:
        super().__init__(images, sizes, pos, ground, height, speed, jump, mass, lives,
                         death_sound, frame_time, is_moving, play_anime, on_screen, grounded,
                         jumpable, is_move, static, jumped, right, big)
        self.coins: int = coins
        self.coin_limit: int = coin_limit
        coinbar_pos: tuple[float, float] = self.live_bar.pos[0], self.live_bar.pos[1] + self.live_bar.sizes[1]
        self.coin_bar: CounterItems = CounterItems(self.fnt_size, self.fnt_path,
                                                   'Coins: ', pos=coinbar_pos, static=True)

    def draw_options(self, wnd) -> None:
        super().draw_options(wnd)
        self.coin_bar.draw(wnd)

    def shift(self, dx: float = 0, dy: float = 0) -> None:
        super().shift(dx, dy)
        self.coin_bar.shift(dx, dy)

    def update_options(self) -> None:
        super().update_options()
        self.to_lives()
        self.coin_bar.update()
        self.coin_bar.counter.change_text(str(self.coins))

    def to_lives(self) -> None:
        if self.coins >= self.coin_limit:
            self.lives += 1
            self.coins -= self.coin_limit

    def __del__(self) -> None:
        pass


class Model7(Model6):
    def __init__(self, base_images,
                 fireman_images,
                 sizes: tuple[float, float],
                 pos: tuple[float, float],
                 ground: float,
                 height: float,
                 speed: float,
                 jump: float,
                 mass: float,
                 coin_limit: int = 10,
                 coins: int = 0,
                 lives: int = 3,
                 death_sound = None,
                 frame_time: float = .15,
                 is_moving: bool = False,
                 play_anime: bool = True,
                 fireform: bool = False,
                 on_screen: bool = True,
                 grounded: bool = False,
                 jumpable: bool = True,
                 is_move: bool = True,
                 static: bool = False,
                 jumped: bool = False,
                 right: bool = True,
                 big: bool = False) -> None:
        super().__init__(base_images, sizes, pos, ground, height, speed, jump, mass, coin_limit, coins,
                         lives, death_sound, frame_time, is_moving, play_anime, on_screen, grounded, jumpable,
                         is_move, static, jumped, right, big)
        self.fire_skin: Skin = Skin(fireman_images, sizes, frame_time, right)
        firespawn: SpawnerFiregun = SpawnerFiregun(right, equiped=True)
        self.firegun = firespawn.spawn()
        self.fireform: bool = fireform
        sizes: Sizes = Sizes()
        firebar_pos: tuple[float, float] = self.fnt_size, sizes.wnd_size[1] - self.fnt_size * 3
        self.fire_bar: CounterItems = CounterItems(self.fnt_size, self.fnt_path, 
                                                   'Bullets: ', pos=firebar_pos, static=True)
    
    def draw_options(self, wnd) -> None:
        super().draw_options(wnd)
        if self.fireform:
            self.fire_bar.draw(wnd)
    
    def shift(self, dx: float = 0, dy: float = 0) -> None:
        super().shift(dx, dy)
        self.fire_bar.shift(dx, dy)
    
    def update_options(self) -> None:
        super().update_options()
        self.fire_bar.update()
        self.fire_bar.counter.change_text(str(self.firegun.bullets))
    
    def key_shoot(self, bullets_list) -> None:
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self.shooting(bullets_list)
    
    def shooting(self, bullets_list) -> None:
        if self.fireform:
            self.firing(bullets_list)
    
    def firing(self, bullets_list) -> None:
        self.firegun.recharge()
        pos: tuple[float, float] = self.rect.left, self.rect.top
        sizes: tuple[float, float] = self.rect.width, self.rect.height
        self.firegun.shoot(pos, sizes, bullets_list)
        if self.firegun.bullets <= 0:
            self.fireform = False

    def change_image(self, animate: bool = True) -> None:
        if self.drawable.in_bound and self.play_anime:
            self.image_options(animate)

    def image_options(self, animate: bool = True) -> None:
        if self.fireform:
            self.image = self.fire_skin.get_image(animate)
        else:
            self.image = self.skin.get_image(animate)

    def respawn_options(self, pos: tuple[float, float]) -> None:
        super().respawn_options(pos)
        self.firegun.bullets = 0
        self.fireform = False

    def pure_resize(self, sizes: tuple[float, float]) -> None:
        super().pure_resize(sizes)
        self.fire_skin.total_resize(sizes)

    def sync_right(self) -> None:
        super().sync_right()
        self.firegun.right = self.right
        self.fire_skin.right = self.right
        self.fire_skin.sync_right()

    def __del__(self) -> None:
        pass
