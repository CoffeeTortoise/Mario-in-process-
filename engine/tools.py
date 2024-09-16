from typing import Callable
from functools import wraps
from random import randint
import pygame as pg
import time as tm


def timer(func: Callable) -> Callable:
    """Returns the execution time of the function"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> float:
        start_time: float = tm.perf_counter()
        func(*args, **kwargs)
        end_time: float = tm.perf_counter()
        elapsed: float = end_time - start_time
        return elapsed
    return wrapper


class Timer:
    """A class for storing time"""
    def __init__(self) -> None:
        self.__buffer: float = 0
        self.__last: float = 0
        self.__whole: bool = False
    
    def get_time(self) -> float:
        if not self.__whole:
            self.__last = tm.perf_counter()
            self.__whole = True
        else:
            current: float = tm.perf_counter()
            delta: float = current - self.__last
            self.__buffer += delta
            self.__whole = False
        return self.__buffer
    
    def restart(self) -> float:
        elapsed_time: float = self.get_time()
        self.__buffer = 0
        return elapsed_time
            
    
    @property
    def buffer(self) -> float:
        return self.__buffer
    
    def __del__(self) -> None:
        pass


class Animator:
    """A class for creating animations. Accepts a list of pygame images, you can adjust the frame time 
    and image sizes. By deafult, the images have the right (current orientation)"""
    def __init__(self, images,
                 sizes: tuple[float, float], 
                 k_time: float = .15,
                 right: bool = True) -> None:
        self.__images = []
        for imag in images:
            imag.set_colorkey((255, 255, 255))
            image = pg.transform.scale(imag, sizes)
            if not right:
                image = pg.transform.flip(image, True, False)
            self.__images.append(image)
        self.__buffer: float = 0
        self.__k_time: float = k_time
        self.__length: float = len(self.__images) - 1
        self.ended: bool = False
    
    def play(self):
        self.__buffer += self.__k_time
        index: int = int(self.__buffer)
        self.ended: bool = False
        if index > self.__length:
            self.ended: bool = True
            self.__buffer = 0
            index = 0
        return self.__images[index]
    
    def total_resize(self, sizes: tuple[float, float]) -> None:
        for i, image in enumerate(self.__images):
            image = pg.transform.scale(image, sizes)
            self.__images[i] = image
    
    def total_flip(self, flip_x: bool = True,
                   flip_y: bool = False) -> None:
        for i, image in enumerate(self.__images):
            image = pg.transform.flip(image, flip_x, flip_y)
            self.__images[i] = image

    def total_rotate(self, degree: float) -> None:
        for i, image in enumerate(self.__images):
            image = pg.transform.rotate(image, degree)
            self.__images[i] = image
    
    def __del__(self) -> None:
        pass


class Camera:
    def __init__(self, 
                 pos: tuple[float, float] = (0, 0),
                 distance_x1: float = 0,
                 distance_x2: float = 0,
                 distance_y: float = 0) -> None:
        self.distance_x1: float = distance_x1
        self.distance_x2: float = distance_x2
        self.distance_y: float = distance_y
        self.pos: tuple[float, float] = pos
    
    def world_shift(self, target, world_objects) -> None:
        offset: tuple[float, float] = self.get_offset(target)
        target.shift(offset[0], offset[1])
        for subject in world_objects:
            if subject is not None:
                subject.shifts(offset[0], offset[1])
    
    def get_offset(self, target) -> tuple[float, float]:
        delta: tuple[float, float] = self.delta(target)
        offset_x: float = self.offset_x(target, delta[0])
        offset_y: float = self.offset_y(target, delta[1])
        return -offset_x, -offset_y
    
    def delta(self, target) -> tuple[float, float]:
        dx: float = target.pos[0] - self.pos[0]
        dy: float = target.pos[1] - self.pos[1]
        return dx, dy
    
    def offset_x(self, target, dx: float) -> float:
        if target.right:
            offset: float =  dx - self.distance_x1
        else:
            offset: float = dx - self.distance_x2
        return offset
    
    def offset_y(self, target, dy: float) -> float:
        offset: float = dy + target.sizes[1] - self.distance_y
        return offset
    
    def __del__(self) -> None:
        pass


class Turntable:
    def __init__(self, music,
                 start: bool = True,
                 mute: bool = False) -> None:
        self.music = music
        self.__start: bool = start
        self.__mute: bool = mute
    
    def update(self) -> None:
        self.turn_on()
        self.turn_off()
    
    def turn_on(self) -> None:
        if self.__start:
            self.music.play(-1)
            self.__start = False
            self.__mute = False
    
    def turn_off(self) -> None:
        if self.__mute:
            self.music.stop()
            self.__mute = False
    
    def resume(self) -> None:
        if self.__mute:
            self.__mute = False
            self.__start = True
    
    def __del__(self) -> None:
        pass


class Soundman:
    def __init__(self, sound, played: bool = False) -> None:
        self.sound = sound
        self.played: bool = played
    
    def play(self) -> None:
        if not self.played:
            self.sound.play()
            self.played = True
    
    def __del__(self) -> None:
        pass
                

class RandPos:
    
    @staticmethod
    def rand_num(begin: int, end: int) -> int:
        if begin > end:
            a: int = int(end)
            b: int = int(begin)
        else:
            a: int = int(begin)
            b: int = int(end)
        num: int = randint(int(begin), int(end))
        return num
    
    @staticmethod
    def rand_pos(bound_x: tuple[int, int], bound_y: tuple[int, int]) -> tuple[int, int]:
        num1: int = RandPos.rand_num(bound_x[0], bound_x[1])
        num2: int = RandPos.rand_num(bound_y[0], bound_y[1])
        return num1, num2
 