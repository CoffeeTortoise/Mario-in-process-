from engine.interfaces import GhostSprite
from engine.enumerations import EntityName
from engine.component import Drawable
from engine.tools import Animator
import pygame as pg


class Picture:
    def __init__(self, image,
                 right: bool = True) -> None:
        if right:
            self.normal = image
            self.flipped = pg.transform.flip(image, True, False)
        else:
            self.flipped = image
            self.normal = pg.transform.flip(image, True, False)
        self.right: bool = right
    
    def change_image(self):
        if self.right:
            return self.normal
        else:
            return self.flipped
    
    def __del__(self) -> None:
        pass


class Cover:
    """A class for managing an object of the Picture class. Skin for single-frame sprites"""
    def __init__(self, image, 
                 sizes: tuple[float, float],
                 right: bool = True) -> None:
        image.set_colorkey((255, 255, 255))
        image = pg.transform.scale(image, sizes)
        self.image: Picture = Picture(image, right)
        self.right: bool = right

    def total_resize(self, sizes: tuple[float, float]) -> None:
        cur_size: tuple[int, int] = self.image.normal.get_size()
        if sizes != cur_size:
            self.image.normal = pg.transform.scale(self.image.normal, sizes)
            self.image.flipped = pg.transform.scale(self.image.flipped, sizes)

    def total_flip(self, flip_x: bool = True, flip_y: bool = False) -> None:
        self.image.normal = pg.transform.flip(self.image.normal, flip_x, flip_y)
        self.image.flipped = pg.transform.flip(self.image.flipped, flip_x, flip_y)
        if flip_x:
            self.right = not self.right
            self.sync_right()

    def sync_right(self) -> None:
        self.image.right = self.right

    def total_rotate(self, degree: float) -> None:
        self.image.normal = pg.transform.rotate(self.image.normal, degree)
        self.image.flipped = pg.transform.rotate(self.image.flipped, degree)

    def get_image(self):
        if self.right:
            return self.image.normal
        else:
            return self.image.flipped

    def get_rect(self):
        return self.image.normal.get_rect()

    def __del__(self) -> None:
        pass


class Imagery(GhostSprite):
    """A class fow working with an image and it's rectangle. The image has 1 view. Image is loaded 
    pygame image from bmp file"""
    def __init__(self, image,
                 sizes: tuple[float, float],
                 pos: tuple[float, float],
                 right: bool = True) -> None:
        self.picture: Cover = Cover(image, sizes, right)
        self.image = self.picture.get_image()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos[0], pos[1]
        self._name: int = EntityName.other
    
    def update(self) -> None:
        print('Nothing to do with me...')
    
    def draw(self, wnd) -> None:
        wnd.blit(self.image, self.rect)
    
    def shift(self, dx: float = 0, dy: float = 0) -> None:
        self.rect.move_ip(dx, dy)
    
    @property
    def name(self) -> int:
        return self._name
    
    @property
    def sizes(self) -> tuple[float, float]:
        return self.rect.width, self.rect.height
    
    @sizes.setter
    def sizes(self, new: tuple[float, float]) -> None:
        x: float = self.rect.left
        y: float = self.rect.top
        h: float = self.rect.height
        dy: float = new[1] - h
        self.picture.total_resize(new)
        self.rect = self.picture.get_rect()
        self.rect.left, self.rect.top = x, y - dy
    
    @property
    def pos(self) -> tuple[float, float]:
        return self.rect.left, self.rect.top
    
    @pos.setter
    def pos(self, new: tuple[float, float]) -> None:
        self.rect.left, self.rect.top = new
    
    def __del__(self) -> None:
        pass


class Sprite(Imagery):
    """A class for better control over the image. Based on the Imagery class. The image can look to the right 
    or to the left. If the image is static, it will not move using the shift method. Image will be rendered 
    only if it is on the screen."""
    def __init__(self, image,
                 sizes: tuple[float, float],
                 pos: tuple[float, float],
                 on_screen: bool = True,
                 static: bool = False,
                 right: bool = True) -> None:
        super().__init__(image, sizes, pos, right)
        self.drawable: Drawable = Drawable(in_bound=on_screen)
        self.right: bool = right
        self.static: bool = static
    
    def draw(self, wnd) -> None:
        if self.drawable.in_bound:
            super().draw(wnd)
    
    def shift(self, dx: float = 0, dy: float = 0) -> None:
        if not self.static:
            super().shift(dx, dy)
    
    def update(self) -> None:
        pos: tuple[float, float] = self.rect.left, self.rect.top
        self.drawable.check_bound(pos)
        self.sync_right()
        self.change_image()
    
    def change_image(self) -> None:
        self.image = self.picture.get_image()
    
    def sync_right(self) -> None:
        self.picture.right = self.right
        self.picture.sync_right()
    
    def total_resize(self, sizes: tuple[float, float]) -> None:
        cur_sizes: tuple[float, float] = self.rect.width, self.rect.height
        if sizes != cur_sizes:
            self.pure_resize(sizes)

    def pure_resize(self, sizes: tuple[float, float]) -> None:
        x: float = self.rect.left
        y: float = self.rect.top
        h: float = self.rect.height
        dy: float = sizes[1] - h
        self.picture.total_resize(sizes)
        self.rect = self.picture.get_rect()
        self.rect.left, self.rect.top = x, y - dy
    
    def __del__(self) -> None:
        pass


class Skin:
    """A skin for a character with multiple frames"""
    def __init__(self, images,
             sizes: tuple[float, float],
             frame_time: float = .15,
             right: bool = True) -> None:
        self.idle: Cover = Cover(images[0], sizes, right)
        if right:
            self.right_anime: Animator = Animator(images, sizes, frame_time, True)
            self.left_anime: Animator = Animator(images, sizes, frame_time, False)
        else:
            self.right_anime: Animator = Animator(images, sizes, frame_time, False)
            self.left_anime: Animator = Animator(images, sizes, frame_time, True)
        self.right: bool = right

    def total_resize(self, sizes: tuple[float, float]) -> None:
        cur_size: tuple[int, int] = self.idle.image.normal.get_size()
        if sizes != cur_size:
            self.idle.total_resize(sizes)
            self.right_anime.total_resize(sizes)
            self.left_anime.total_resize(sizes)

    def total_flip(self, flip_x: bool = True,
                   flip_y: bool = False) -> None:
        self.idle.total_flip(flip_x, flip_y)
        self.right_anime.total_flip(flip_x, flip_y)
        self.left_anime.total_flip(flip_x, flip_y)
        if self.flip_x:
            self.right = not self.right

    def sync_right(self) -> None:
        self.idle.right = self.right
        self.idle.sync_right()

    def total_rotate(self, degree: float) -> None:
        self.idle.total_rotate(degree)
        self.right_anime.total_rotate(degree)
        self.left_anime.total_rotate(degree)

    def get_anime(self):
        if self.right:
            image = self.right_anime.play()
        else:
            image = self.left_anime.play()
        return image

    def get_image(self, play_anime: bool = True):
        if play_anime:
            image = self.get_anime()
        else:
            image = self.idle.get_image()
        return image

    def get_rect(self):
        return self.idle.get_rect()

    def __del__(self) -> None:
        pass


class AnimatedSprite(GhostSprite):
    """Animated sprite with right and left animation"""
    def __init__(self, images,
                 sizes: tuple[float, float],
                 pos: tuple[float, float],
                 frame_time: float = .15,
                 play_anime: bool = True,
                 on_screen: bool = True,
                 static: bool = False,
                 right: bool = True) -> None:
        self.skin: Skin = Skin(images, sizes, frame_time, right)
        self.image = self.skin.get_image(play_anime=False)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos
        self.drawable: Drawable = Drawable(in_bound=on_screen)
        self._name: int = EntityName.other
        self.right: bool = right
        self.static: bool = static
        self.play_anime: bool = play_anime
        
    def draw(self, wnd) -> None:
        if self.drawable.in_bound:
            wnd.blit(self.image, self.rect)

    def shift(self, dx: float = 0, dy: float = 0) -> None:
        if not self.static:
            self.rect.move_ip(dx, dy)
            
    def update(self) -> None:
        pos: tuple[float, float] = self.rect.left, self.rect.top
        self.drawable.check_bound(pos)
        self.sync_right()
        self.change_image()

    def sync_right(self) -> None:
        self.skin.right = self.right
        self.skin.sync_right()
    
    def total_resize(self, sizes: tuple[float, float]) -> None:
        cur_sizes: tuple[float, float] = self.rect.width, self.rect.height
        if sizes != cur_sizes:
            self.pure_resize(sizes)

    def pure_resize(self, sizes: tuple[float, float]) -> None:
        self.skin.total_resize(sizes)
        pos: tuple[float, float] = self.rect.left, self.rect.top
        self.rect = self.skin.get_rect()
        self.rect.left, self.rect.top = pos

    def change_image(self, animate: bool = True) -> None:
        if self.drawable.in_bound and self.play_anime:
            self.image = self.skin.get_image(animate)
    
    @property
    def name(self) -> int:
        return self._name

    @property
    def sizes(self) -> tuple[float, float]:
        return self.rect.width, self.rect.height
    
    @property
    def pos(self) -> tuple[float, float]:
        return self.rect.left, self.rect.top
    
    @pos.setter
    def pos(self, new: tuple[float, float]) -> None:
        self.rect.left, self.rect.top = new

    def __del__(self) -> None:
        pass
