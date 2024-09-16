from engine.spawner import SpawnerLifeShroom, SpawnerSuperShroom, SpawnerCoin, SpawnerFireFlower
from engine.interfaces import Spawner
from engine.block import MarioBlock
from engine.constants import Sizes
from engine.picture import Cover
from random import randint
import pygame as pg


SIZE: float = Sizes().size


class SurpriseBlock(MarioBlock):
    def __init__(self, image,
                 image2,
                 brick_sound,
                 breakblock_sound,
                 sizes: tuple[float, float],
                 pos: tuple[float, float],
                 destructible: bool = False,
                 in_activity: bool = True,
                 destroyed: bool = False,
                 on_screen: bool = True,
                 unleashed: bool = False,
                 static: bool = False,
                 right: bool = True) -> None:
        super().__init__(image, brick_sound, breakblock_sound, sizes, pos, destructible,
                          in_activity, destroyed, on_screen, static, right)
        self.picture2: Cover = Cover(image2, sizes, right)
        self.unleashed: bool = unleashed
        variant: int = randint(0, 100)
        if (variant >= 0) and (variant <= 65):
            self.spawner = SpawnerCoin()
        elif (variant > 65) and (variant <= 75):
            self.spawner = SpawnerFireFlower()
        elif (variant > 75) and (variant <= 85):
            self.spawner = SpawnerSuperShroom()
        else:
            self.spawner = SpawnerLifeShroom()

    def change_image(self) -> None:
        if not self.unleashed:
            self.image = self.picture.get_image()
        else:
            self.image = self.picture2.get_image()

    def sync_right(self) -> None:
        self.picture.right = self.right
        self.picture.sync_right()
        self.picture2.right = self.right
        self.picture2.sync_right()

    def interact_options(self, target, collection) -> None:
        self.sound_clsn.play()
        if not self.unleashed:
            pos: tuple[float, float] = self.rect.left, self.rect.top - self.spawner.sizes[1]
            item = self.spawner.spawn(pos)
            collection.append(item)
            self.unleashed = True

    def interact(self, target, collection) -> None:
        check_active: bool = target.rect.colliderect(self.rect) and self.updatable.in_bound
        if check_active and not self.destroyed:
            self.interact_options(target, collection)

    def __del__(self) -> None:
        pass


class SpawnerSurpriseBlock(Spawner):
    def __init__(self) -> None:
        image_path: str = 'Assets/Sprites/Blocks/Polys/SurpriseBlock/0.bmp'
        image2_path: str = 'Assets/Sprites/Blocks/Polys/SurpriseBlock/1.bmp'
        brick_snd_path: str = 'Assets/Music/brick.ogg'
        break_snd_path: str = 'Assets/Music/breakblock.ogg'
        self.__image = pg.image.load(image_path).convert()
        self.__image2 = pg.image.load(image2_path).convert()
        self.__brick_sound = pg.mixer.Sound(brick_snd_path)
        self.__break_sound = pg.mixer.Sound(break_snd_path)
        self.__sizes: tuple[float, float] = SIZE, SIZE

    def spawn(self, pos) -> SurpriseBlock:
        return SurpriseBlock(self.__image, self.__image2, self.__brick_sound, self.__break_sound, self.__sizes, pos)

    @property
    def sizes(self) -> tuple[float, float]:
        return self.__sizes

    def __del__(self) -> None:
        pass
