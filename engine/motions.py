from engine.enumerations import ProcStatus
from engine.tools import RandPos, Timer
from engine.component import Delta
import pygame as pg
import math as mt


class Circle:
    def __init__(self, speed: float,
                  max_speed: float,
                  radius: float,
                  center: tuple[float, float],
                  initial_angle: float = 0,
                  clockwise: bool = True) -> None:
        if abs(speed) > mt.pi * 2:
            speed = mt.pi / 64
        if abs(max_speed) > mt.pi * 2:
            max_speed = mt.pi / 64
        if abs(initial_angle) >= mt.pi * 2:
            initial_angle = 0
        self.speed: Delta = Delta(speed, max_speed)
        self.radius: float = radius
        self.clockwise: bool = clockwise
        self.center: tuple[float, float] = center
        self.__t: float = initial_angle

    def move_rect(self, rect) -> tuple[float, float]:
        offset: tuple[float, float] = self.get_offset(rect)
        rect.move_ip(offset[0], offset[1])
        return offset

    def get_offset(self, rect) -> tuple[float, float]:
        self.set_angle()
        x: float = self.center[0] + self.radius * mt.cos(self.__t)
        y: float = self.center[1] + self.radius * mt.sin(self.__t)
        dx: float = x - rect.centerx
        dy: float = y - rect.centery
        return dx, dy

    def set_angle(self) -> None:
        da: float = self.get_da()
        self.limit_angle()
        self.__t += da

    def get_da(self) -> float:
        """Angle increment"""
        da: float = self.speed.get_current()
        if (da < 0) and self.clockwise:
            da *= -1
        if (da > 0) and not self.clockwise:
            da *= -1
        return da

    def limit_angle(self) -> None:
        if abs(self.__t) >= mt.pi * 2:
            self.__t = 0

    def shift_center(self, dx: float = 0, dy: float = 0) -> None:
        x: float = self.center[0] + dx
        y: float = self.center[1] + dy
        self.center = x, y

    def __del__(self) -> None:
        pass


class Rotation:
    def __init__(self, image,
                 sizes: tuple[float, float],
                 pos: tuple[float, float],
                 moments: int = 12,
                 speed: float = .15,
                 clockwise: bool = True) -> None:
        self.__sizes: tuple[float, float] = sizes
        self.__pos: tuple[float, float] = pos
        self.__max_ind: int = moments - 1
        self.__speed: float = speed
        self.__ind: float = 0
        self.__rotation = []
        delta: float = 360 / moments
        image.set_colorkey((255, 255, 255))
        image = pg.transform.scale(image, sizes)
        for i in range(1, moments + 1):
            angle: float = delta * i
            rotated_image = pg.transform.rotate(image, angle)
            if clockwise:
                rotated_image = pg.transform.flip(rotated_image, True, False)
            rect = rotated_image.get_rect()
            rect.center = pos
            self.__rotation.append([rotated_image, rect])

    def rotate(self):
        self.__ind += self.__speed
        index: int = int(self.__ind)
        if index > self.__max_ind:
            index = 0
            self.__ind = 0
        return self.__rotation[index]

    def shift_center(self, dx: float = 0, dy: float = 0) -> None:
        pos: tuple[float, float] = self.__pos[0] + dx, self.__pos[1] + dy
        self.set_center(pos)

    def set_center(self, pos: tuple[float, float]) -> None:
        if pos != self.__pos:
            self.__pos = pos
            for i, _ in enumerate(self.__rotation):
                self.__rotation[i][1].center = pos

    def total_resize(self, sizes: tuple[float, float]) -> None:
        if sizes != self.__sizes:
            delta_y: float = (self.__sizes[1] - sizes[1]) * .5
            self.__sizes = sizes
            self.__pos = self.__pos[0], self.__pos[1] + delta_y
            for i, pair in enumerate(self.__rotation):
                pair[0] = pg.transform.scale(pair[0], sizes)
                pair[1] = pair[0].get_rect()
                pair[1].center = self.__pos
                self.__rotation[i] = pair

    def total_flip(self, flip_x: bool = True, flip_y: bool = False) -> None:
        for i, pair in enumerate(self.__rotation):
            pair[0] = pg.transform.flip(pair[0], flip_x, flip_y)
            pair[1] = pair[0].get_rect()
            pair[1].center = self.__pos
            self.__rotation[i] = pair

    @property
    def pos(self) -> tuple[float, float]:
        """Center of rotation"""
        return self.__pos

    @property
    def sizes(self) -> tuple[float, float]:
        return self.__sizes

    def __del__(self) -> None:
        pass
        

class Patrol:
    def __init__(self,
                 speed: float,
                 max_speed: float,
                 length: float,
                 initial_coordinate: float,
                 vertical: bool = False,
                 round1: bool = True) -> None:
        self.speed: Delta = Delta(speed, max_speed)
        self.begin: float = initial_coordinate
        if round1:
            self.end: float = self.begin + length
        else:
            self.end: float = self.begin - length
        self.vertical: bool = vertical
        self.forward: bool = round1
        self.round1: bool = round1

    def move_rect(self, rect) -> float:
        offset: float = self.patrol(rect)
        if self.vertical:
            rect.move_ip(0, offset)
        else:
            rect.move_ip(offset, 0)
        return offset

    def patrol(self, rect) -> float:
        pos: float = self.get_rect_pos(rect)
        status: int = 0
        if (pos <= self.begin) and self.round1:
            self.forward = True
        elif ((pos >= self.begin) and (pos < self.end)) and self.round1:
            self.forward = True
        elif (pos >= self.end) and self.round1:
            self.forward = True
            self.round1 = False
        elif (pos >= self.end) and not self.round1:
            self.forward = False
        elif ((pos <= self.end) and (pos > self.begin)) and not self.round1:
            self.forward = False
        elif (pos <= self.begin) and not self.round1:
            self.forward = False
            self.round1 = True
        else:
            status = 2
        offset: float = self.get_offset()
        if status == ProcStatus.stuck:
            offset = 0
        return offset

    def get_rect_pos(self, rect) -> float:
        if self.vertical:
            pos: float = rect.centery
        else:
            pos: float = rect.centerx
        return pos

    def get_offset(self) -> float:
        """Forward means to right if horizontal, and down if vertical"""
        offset: float = self.speed.get_current()
        if (offset < 0) and self.forward:
            offset *= -1
        if (offset > 0) and not self.forward:
            offset *= -1
        return offset

    def shift_patrol(self, dx: float = 0, dy: float = 0) -> None:
        if self.vertical:
            self.begin += dy
            self.end += dy
        else:
            self.begin += dx
            self.end += dx

    def __del__(self) -> None:
        pass


class Drip:
    def __init__(self,
                 speed: float,
                 max_speed: float,
                 middle_line: float,
                 bounds_x: tuple[float, float],
                 bounds_y: tuple[float, float]) -> None:
        if speed < 0:
            speed *= -1
        if max_speed < 0:
            max_speed *= -1
        self.__speed: Delta = Delta(speed, max_speed)
        self.__middle_line: float = middle_line
        self.__bounds_x: tuple[float, float] = bounds_x
        self.__bounds_y: tuple[float, float] = bounds_y
        self.__fall: bool = False
    
    def move_rect(self, rect) -> None:
        self.start_fall(rect)
        speed: float = self.__speed.get_current()
        rect.move_ip(0, speed)
        self.end_fall(rect)
    
    def end_fall(self, rect) -> None:
        y: float = rect.centery
        if y >= self.__bounds_y[1]:
            self.__fall = False
    
    def start_fall(self, rect) -> None:
        if not self.__fall:
            rect.center = self.get_start_pos()
            self.__fall = True
    
    def get_start_pos(self) -> tuple[int, int]:
        bound_y: tuple[float, float] = self.__bounds_y[0], self.__middle_line
        pos: tuple[float, float] = RandPos.rand_pos(self.__bounds_x, bound_y)
        return pos
    
    def __del__(self) -> None:
        pass


class Parabola:
    """Give argument fly_angle in degrees"""
    def __init__(self,
                 speed: float,
                 max_speed: float,
                 fly_angle: float,
                 right: bool = True,
                 down: bool = True) -> None:
        self.speed: Delta = Delta(speed, max_speed)
        self.fly_angle: float = mt.radians(fly_angle)
        self.__lim: float = mt.pi * .5
        self.right: bool = right
        self.down: bool = down
    
    def move_rect(self, rect, special: bool = False) -> tuple[float, float]:
        offset: tuple[float, float] = self.get_offset(special)
        rect.move_ip(offset[0], offset[1])
        return offset
    
    def get_offset(self, special: bool = False) -> tuple[float, float]:
        angle: float = self.fix_angle(special)
        speed: float = self.speed.get_current()
        dx: float = speed * mt.cos(angle)
        dy: float = speed * mt.sin(angle)
        dy: float = self.fix_dy(dy)
        return dx, dy
    
    def fix_dy(self, dy) -> float:
        """Corrects movement to down or up"""
        if (dy < 0) and self.down:
            dy *= -1
        if (dy > 0) and not self.down:
            dy *= -1
        return dy
    
    def fix_angle(self, special: bool = False) -> float:
        """Corrects the angle for right and left movement"""
        angle: float = self.fly_angle
        if (self.fly_angle > self.__lim) and self.right:
            angle -= self.__lim
        if ((self.fly_angle < self.__lim) and not special) and not self.right:
            angle += self.__lim
        if special and not self.right:
            angle += self.__lim
        return angle
    
    def __del__(self) -> None:
        pass
