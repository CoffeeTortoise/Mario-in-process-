from engine.enumerations import EntityName
from engine.interfaces import GhostSprite
from engine.component import Drawable
import pygame as pg


class RectangleShape(GhostSprite):
    def __init__(self,
                 pos: tuple[float, float],
                 sizes: tuple[float, float],
                 color: tuple[int, ...],
                 line_width: int = 0) -> None:
        self.drawable: Drawable = Drawable()
        self.__pos: tuple[float, float] = pos
        self.__sizes: tuple[float, float] = sizes
        self.__color: tuple[int, ...] = color
        self.__line_width: int = line_width
        self._name: int = EntityName.other
    
    def draw(self, wnd) -> None:
        if self.drawable.in_bound:
            rect = pg.rect.Rect(self.__pos[0], self.__pos[1], self.__sizes[0], self.__sizes[1])
            pg.draw.rect(wnd, self.__color, rect, self.__line_width)
    
    def shift(self, dx: float = 0, dy: float = 0) -> None:
        pos: tuple[float, float] = self.__pos[0] + dx, self.__pos[1] + dy
        self.set_pos(pos)
    
    def update(self) -> None:
        self.drawable.check_bound(self.__pos)
    
    def set_pos(self, pos: tuple[float, float]) -> None:
        if pos != self.__pos:
            self.__pos = pos
    
    def set_sizes(self, sizes: tuple[float, float]) -> None:
        if sizes != self.__sizes:
            self.__sizes = sizes
    
    def set_color(self, color: tuple[int, ...]) -> None:
        if color != self.__color:
            self.__color = color
    
    def set_line_width(self, line_width: int) -> None:
        if line_width != self.__line_width:
            self.__line_width = line_width
    
    @property
    def pos(self) -> tuple[float, float]:
        return self.__pos
    
    @property
    def sizes(self) -> tuple[float, float]:
        return self.__sizes
    
    @property
    def color(self) -> tuple[int, ...]:
        return self.__color
    
    @property
    def line_width(self) -> int:
        return self.__line_width
    
    @property
    def rect(self):
        return pg.rect.Rect(self.__pos[0], self.__pos[1], self.__sizes[0], self.__sizes[1])
    
    @property
    def name(self) -> int:
        return self._name
    
    def __del__(self) -> None:
        pass


class CircleShape(GhostSprite):
    def __init__(self,
                 radius: float,
                 color: tuple[int, ...],
                 center: tuple[float, float],
                 line_width: int = 0) -> None:
        self.drawable: Drawable = Drawable()
        self.__center: tuple[float, float] = center
        self.__color: tuple[int, ...] = color
        self.__radius: float = radius
        self.__line_width: int = line_width
        self._name: int = EntityName.other
    
    def draw(self, wnd) -> None:
        if self.drawable.in_bound:
            pg.draw.circle(wnd, self.__color, self.__center, self.__radius, self.__line_width)
    
    def shift(self, dx: float = 0, dy: float = 0) -> None:
        center: tuple[float, float] = self.__center[0] + dx, self.__center[1] + dy
        self.set_center(center)
    
    def update(self) -> None:
        self.drawable.check_bound(self.__center)
    
    def set_center(self, center: tuple[float, float]) -> None:
        if center != self.__center:
            self.__center = center
    
    def set_color(self, color: tuple[int, ...]) -> None:
        if color != self.__color:
            self.__color = color
    
    def set_radius(self, radius: float) -> None:
        if radius != self.__radius:
            self.__radius = radius
    
    def set_line_width(self, line_width: int) -> None:
        if line_width != self.__line_width:
            self.__line_width = line_width
    
    @property
    def pos(self) -> tuple[float, float]:
        """Center of the circle"""
        return self.__center
    
    @property
    def sizes(self) -> tuple[float, float]:
        """The sizes of the corresponding rectangle"""
        return self.__radius * 2, self.__radius * 2

    @property
    def color(self) -> tuple[int, ...]:
        return self.__color
    
    @property
    def radius(self) -> float:
        return self.__radius
    
    @property
    def line_width(self) -> int:
        return self.__line_width
    
    @property
    def rect(self):
        """Corresponding rectangle"""
        left: float = self.__center[0] - self.__radius
        top: float = self.__center[1] - self.__radius
        sizes: tuple[float, float] = self.__radius * 2, self.__radius * 2
        return pg.rect.Rect(left, top, sizes[0], sizes[1])
    
    @property
    def name(self) -> int:
        return self._name
    
    def __del__(self) -> None:
        pass
