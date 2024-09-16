import pygame as pg
pg.init()


class Sizes:
    """A class for storing basic sizes"""
    def __init__(self) -> None:
        info = pg.display.Info()
        raw_sizes: tuple[float, float] = info.current_w, info.current_h
        self.__rows: int = 12
        self.__cols: int = 22
        self.__size: float = raw_sizes[1] / self.__rows
        wnd_w: float = self.__cols * self.__size
        wnd_h: float = self.__rows * self.__size
        self.__wnd_size: tuple[float, float] = wnd_w, wnd_h
    
    @property
    def rows(self) -> int:
        return self.__rows
    
    @property
    def cols(self) -> int:
        return self.__cols
    
    @property
    def size(self) -> float:
        return self.__size
    
    @property
    def wnd_size(self) -> tuple[float, float]:
        return self.__wnd_size
    
    def __del__(self) -> None:
        pass


class DrawBounds:
    """A class for storing drawing borders"""
    def __init__(self) -> None:
        sizes: Sizes = Sizes()
        x1: float = -sizes.size * 5
        x2: float = sizes.wnd_size[0] + sizes.size * 5
        self.__bound_x: tuple[float, float] = x1, x2
        y1: float = -sizes.size * 5
        y2: float = sizes.wnd_size[1] + sizes.size * 5
        self.__bound_y: tuple[float, float] = y1, y2
    
    @property
    def bound_x(self) -> tuple[float, float]:
        return self.__bound_x
    
    @property
    def bound_y(self) -> tuple[float, float]:
        return self.__bound_y
    
    def __del__(self) -> None:
        pass


class UpdateBounds:
    """A class for storing activity boundaries (update method)"""
    def __init__(self) -> None:
        sizes: Sizes = Sizes()
        x1: float = -sizes.wnd_size[0]
        x2: float = sizes.wnd_size[0] * 2
        self.__bound_x: tuple[float , float] = x1, x2
        y1: float = -sizes.size * 5
        y2: float = sizes.wnd_size[1] + sizes.size * 5
        self.__bound_y: tuple[float, float] = y1, y2
    
    @property
    def bound_x(self) -> tuple[float, float]:
        return self.__bound_x
    
    @property
    def bound_y(self) -> tuple[float, float]:
        return self.__bound_y
    
    def __del__(self) -> None:
        pass


class FPSer:
    """A class for storing the recommended fps and frame time"""
    def __init__(self) -> None:
        self.__fps1: int = 30
        self.__fps2: int = 60
        self.__frT1: float = 10 / self.__fps1
        self.__frT2: float = 10 / self.__fps2
    
    @property
    def fps1(self) -> int:
        return self.__fps1
    
    @property
    def fps2(self) -> int:
        return self.__fps2
    
    @property
    def fr_t1(self) -> float:
        return self.__frT1
    
    @property
    def fr_t2(self) -> float:
        return self.__frT2
    
    def __del__(self) -> None:
        pass
