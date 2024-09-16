from engine.component import Drawable
import pygame as pg


class Text:
    def __init__(self,
                 txt: str,
                 size: int,
                 fnt_path: str,
                 pos: tuple[float, float] = (0, 0),
                 color: tuple[int, ...] | None = None,
                 fnt_color: tuple[int, ...] = (255, 255, 255)) -> None:
        self.__txt: str = txt
        self.__size: int = size
        self.__fnt_path: str = fnt_path
        self.__fnt_color: tuple[int, ...] = fnt_color
        self.__color: tuple[int, ...] | None = color
        self.__font = pg.font.Font(fnt_path, size)
        if color is None:
            self.text = self.__font.render(self.__txt, 1, self.__fnt_color)
            self.__filled: bool = False
        else:
            self.text = self.__font.render(self.__txt, 1, self.__fnt_color, color)
            self.__filled: bool = True
        pos: tuple[float, float] = pos
        self.rect = self.text.get_rect()
        self.rect.left, self.rect.top = pos
    
    def draw(self, wnd) -> None:
        wnd.blit(self.text, self.rect)
    
    def update(self) -> None:
        pass
    
    def shift(self, dx: float = 0, dy: float = 0) -> None:
        self.rect.move_ip(dx, dy)
    
    def change_text(self, txt: str) -> None:
        if self.__txt != txt:
            self.__txt = txt
            self.update_text()
    
    def update_text(self) -> None:
        if self.__filled:
            self.text = self.__font.render(self.__txt, 1, self.__fnt_color, self.__color)
        else:
            self.text = self.__font.render(self.__txt, 1, self.__fnt_color)
        self.update_pos()
    
    def update_pos(self) -> None:
        pos: tuple[float, float] = self.rect.left, self.rect.top
        self.rect = self.text.get_rect()
        self.rect.left, self.rect.top = pos
    
    def change_fnt(self, fnt_path: str) -> None:
        if self.__fnt_path != fnt_path:
            self.__font = pg.font.Font(fnt_path, self.__size)
            self.__fnt_path = fnt_path
            self.update_text()
    
    def change_fnt_color(self, fnt_color: tuple[int, ...]) -> None:
        if self.__fnt_color != fnt_color:
            self.__fnt_color = fnt_color
            self.update_text()
    
    def change_fnt_size(self, size: int) -> None:
        if self.__size != size:
            self.__size = size
            self.__font = pg.font.Font(self.__fnt_path, size)
            self.update_text()
    
    def change_color(self, color: tuple[int, ...] | None) -> None:
        if self.__color != color:
            self.__color = color
            self.check_filled(color)
            self.update_text()
    
    def check_filled(self, color: tuple[int, ...] | None) -> None:
        if color is None:
            self.__filled = False
        else:
            self.__filled = True
    
    @property
    def pos(self) -> tuple[float, float]:
        return self.rect.left, self.rect.top
    
    @pos.setter
    def pos(self, new: tuple[float, float]) -> None:
        self.rect.left, self.rect.top = new
    
    @property
    def sizes(self) -> tuple[float, float]:
        return self.rect.width, self.rect.height
    
    def __del__(self) -> None:
        pass


class Inscription(Text):
    def __init__(self,
                 txt: str,
                 size: int,
                 fnt_path: str,
                 static: bool = False,
                 on_screen: bool = True,
                 pos: tuple[float, float] = (0, 0),
                 color: tuple[int, ...] | None = None,
                 fnt_color: tuple[int, ...] = (255, 255, 255)) -> None:
        super().__init__(txt, size, fnt_path, pos, color, fnt_color)
        self.drawable: Drawable = Drawable(in_bound=on_screen)
        self.static: bool = static
    
    def draw(self, wnd) -> None:
        if self.drawable.in_bound:
            super().draw(wnd)
    
    def update(self) -> None:
        pos: tuple[float, float] = self.rect.left, self.rect.top
        self.drawable.check_bound(pos)
    
    def shift(self, dx: float = 0, dy: float = 0) -> None:
        if not self.static:
            super().shift(dx, dy)
    
    def __del__(self) -> None:
        pass


class CounterItems:
    def __init__(self,
                 size: int,
                 fnt_path: str,
                 item_name: str,
                 start_num: int = 0,
                 static: bool = False,
                 on_screen: bool = True,
                 pos: tuple[float, float] = (0, 0),
                 color: tuple[int, ...] | None = None,
                 fnt_color: tuple[int, ...] = (255, 255, 255)) -> None:
        self.text: Inscription = Inscription(item_name, size, fnt_path, static, 
                                             on_screen, pos, color, fnt_color)
        counter_x: float = pos[0] + self.text.sizes[0]
        counter_pos: tuple[float, float] = counter_x, pos[1]
        self.counter: Inscription = Inscription(str(start_num), size, fnt_path, static, 
                                             on_screen, counter_pos, color, fnt_color)
    
    def draw(self, wnd) -> None:
        self.text.draw(wnd)
        self.counter.draw(wnd)
    
    def update(self) -> None:
        self.text.update()
        self.counter.update()
    
    def shift(self, dx: float = 0, dy: float = 0) -> None:
        self.text.shift(dx, dy)
        self.counter.shift(dx, dy)
    
    @property
    def rect(self):
        return pg.Rect(self.pos[0], self.pos[1], self.sizes[0], self.sizes[1])
    
    @property
    def sizes(self) -> tuple[float, float]:
        width: float = self.text.sizes[0] + self.counter.sizes[0]
        height: float = self.text.sizes[1]
        return width, height
    
    @property
    def pos(self) -> tuple[float, float]:
        return self.text.pos
    
    @pos.setter
    def pos(self, new: tuple[float, float]) -> None:
        self.text.pos = new
        counter_x: float = new[0] + self.text.sizes[0]
        self.counter.pos = counter_x, new[1]
    
    def __del__(self) -> None:
        pass
