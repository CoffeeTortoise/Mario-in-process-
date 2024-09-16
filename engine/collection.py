from typing import Any


class Collection:
    """A simple class for creating a collection based on a list"""
    def __init__(self) -> None:
        self.__tar: list[Any] = []
    
    def append(self, item: Any) -> None:
        self.__tar.append(item)
    
    def get_index_of(self, item: Any) -> int:
        return self.__tar.index(item)
    
    def delete_item(self, index: int) -> None:
        del self.__tar[index]
    
    def clear(self) -> None:
        self.__tar = []
    
    @property
    def tar(self) -> list[Any]:
        return self.__tar
    
    def __getitem__(self, index: int) -> Any:
        return self.__tar[index]
    
    def __setitem__(self, index: int, item: Any) -> None:
        self.__tar[index] = item
    
    def __len__(self) -> int:
        return len(self.__tar)
    
    def __del__(self) -> None:
        pass


class PictureList(Collection):
    """A class for managing a group of imageries(draws, shifts methods). Based on a class 
    Collection."""
    def __init__(self) -> None:
        super().__init__()
    
    def do_stuff(self, wnd, dx: float = 0, dy: float = 0) -> None:
        for item in self.tar:
            item.draw(wnd)
            item.shift(dx, dy)
    
    def draws(self, wnd) -> None:
        for item in self.tar:
            item.draw(wnd)
    
    def shifts(self, dx: float = 0, dy: float = 0) -> None:
        for item in self.tar:
            item.shift(dx, dy)
    
    def __del__(self) -> None:
        pass


class SpriteList(PictureList):
    """A class for managing a group of sprites(adds updates method). Based on PictureList class."""
    def __init__(self) -> None:
        super().__init__()
    
    def do_stuff(self, wnd, dx: float = 0, dy: float = 0) -> None:
        """Draw, update and shift"""
        for item in self.tar:
            item.update()
            item.draw(wnd)
            item.shift(dx, dy)
    
    def updates(self) -> None:
        for item in self.tar:
            item.update()
    
    def __del__(self) -> None:
        pass


class ActiveSprites(SpriteList):
    """Movable sprites. Reflection means changing the direction of movement to the opposite.
    Objects in this collection must have the to_right attribute if reflectable is True. The speed
    component is required for collection objects"""
    def __init__(self, reflectable: bool = False) -> None:
        super().__init__()
        self.reflectable: bool = reflectable
    
    def physical_stuff(self, wnd, solid_blocks,
                       dx: float = 0, dy: float = 0) -> None:
        """Update, shift and collisions"""
        for item in self.tar:
            item.update()
            item.draw(wnd)
            item.shift(dx, dy)
            solid_blocks.do_collision(item, item.speed.limiter, hor_repulse=self.reflectable)
    
    def collisions(self, solid_blocks) -> None:
        for item in self.tar:
            solid_blocks.do_collision(item, item.speed.limiter, hor_repulse=self.reflectable)
    
    def __del__(self) -> None:
        pass


class InteractiveSprites(ActiveSprites):
    """Based on class ActiveSprites. Items must have the destroyed and physical fields, and their class inherit the
    interactive interface"""
    def __init__(self, reflectable: bool = False) -> None:
        super().__init__(reflectable)
    
    def all_stuff(self, wnd, target, solid_blocks,
                  dx: float = 0, dy: float = 0) -> None:
        """Update, shift, interacts and collisions"""
        for item in self.tar:
            item.update()
            item.draw(wnd)
            item.shift(dx, dy)
            item.interact(target)
            if item.physical and not item.destroyed:
                solid_blocks.do_collision(item, item.speed.limiter, hor_repulse=self.reflectable)
    
    def interacts(self, target) -> None:
        for item in self.tar:
            item.interact(target)
    
    def __del__(self) -> None:
        pass


class BulletsList(InteractiveSprites):
    def __init__(self, reflectable: bool = False) -> None:
        super().__init__(reflectable)
    
    def all_stuff(self, wnd, target, solid_blocks,
                  dx: float = 0, dy: float = 0) -> None:
        """Update, shift, interacts and collisions"""
        for item in self.tar:
            item.update()
            item.draw(wnd)
            item.shift(dx, dy)
            item.interact(target)
            if item.physical and not item.destroyed:
                BulletsList.collide_solids(item, solid_blocks)
    
    def kill_targets(self, targets) -> None:
        for item in self.tar:
            if item.activated and not item.destroyed:
                BulletsList.interact_targets(item, targets)
    
    @staticmethod
    def interact_targets(item, targets) -> None:
        for target in targets:
            if target.rect.colliderect(item.rect):
                BulletsList.interact_options(item, target)
    
    @staticmethod
    def interact_options(item, target) -> None:
        if hasattr(target, 'destroyed') and not target.destroyed:
            BulletsList.destroy_block(item, target)
        else:
            BulletsList.kill_entity(item, target)
    
    @staticmethod
    def kill_entity(item, target) -> None:
        if hasattr(target, 'alive') and target.alive:
            item.interact(target)
    
    @staticmethod
    def collide_solids(item, solid_blocks) -> None:
        """Collisions with Mono/Poly-blocks"""
        for block in solid_blocks:
            if item.rect.colliderect(block.rect) and not block.destroyed:
                BulletsList.destroy_block(item, block)
    
    @staticmethod
    def destroy_block(item, block) -> None:
        if item.activated and not item.destroyed:
            BulletsList.destroy_options(item, block)
    
    @staticmethod
    def destroy_options(item, block) -> None:
        if hasattr(block, 'sound_broken'):
            block.sound_broken.play()
        block.destroyed = True
        item.destroyed = True
        item.static = True
    
    def __del__(self) -> None:
        pass


class HorizontalWalls(SpriteList):
    """A class with horizontal collision control. Based on SpriteList class"""
    def __init__(self) -> None:
        super().__init__()
    
    def hor_collision(self, sprite, limiter: float = 0) -> None:
        for item in self.tar:
            if sprite.rect.colliderect(item.rect):
                self.hor_collide(sprite, item, limiter)
    
    def hor_collide(self, sprite, item,
                    limiter: float = 0,
                    hor_repulse: bool = False) -> None:
        sprite_pos: tuple[float, float] = sprite.pos
        offset: float = item.sizes[0] * .2
        item_x: float = item.pos[0]
        if sprite.right:
            sprite_x: float = item_x - limiter - offset
        else:
            sprite_x: float = item_x + item.sizes[0] + limiter + offset
        sprite.pos = sprite_x, sprite_pos[1]
        self.hor_reflect(sprite, hor_repulse)
    
    @staticmethod
    def hor_reflect(sprite, hor_repulse: bool = False) -> None:
        if hor_repulse:
            sprite.right = not sprite.right
        if hasattr(sprite, 'to_right') and hor_repulse:
            sprite.to_right = not sprite.to_right
    
    def __del__(self) -> None:
        pass


class SolidBlocks(HorizontalWalls):
    """A class for simulating solid blocks (vertical and horizontal collisions). Based on 
    HorizontalWalls class."""
    def __init__(self) -> None:
        super().__init__()
    
    def do_collision(self, sprite,
                     limiter: float = 0,
                     hor_repulse: bool = False) -> None:
        self.fix_jumping(sprite)
        for item in self.tar:
            if sprite.rect.colliderect(item.rect):
                self.correct_hor_collide(sprite, item, limiter, hor_repulse)
                self.ver_collider(sprite, item)
    
    @staticmethod
    def fix_jumping(sprite) -> None:
        if hasattr(sprite, 'jump') and not sprite.jump.in_jumping:
            sprite.gravity.grounded = False
    
    def correct_hor_collide(self, sprite, item, limiter, hor_repulse: bool = False) -> None:
        delta: float = abs(sprite.pos[1] - item.pos[1])
        height: float = item.sizes[1] * .63
        if delta <= height:
            self.hor_collide(sprite, item, limiter, hor_repulse)
            self.correct_offsety(sprite, height)
    
    @staticmethod
    def correct_offsety(sprite, height: float) -> None:
        if hasattr(sprite, 'jump') and sprite.jump.in_jumping:
            y: float = sprite.pos[1]
        else:
            y: float = sprite.pos[1] - height * .1
        sprite.gravity.grounded = False
        sprite.pos = sprite.pos[0], y
    
    def ver_collision(self, sprite) -> None:
        for item in self.tar:
            if sprite.rect.colliderect(item.rect):
                self.ver_collider(sprite, item)
    
    def ver_collider(self, sprite, item) -> None:
        if (sprite.pos[1] < item.pos[1]) and not sprite.gravity.grounded:
            self.ver_collide(sprite, item)
        if sprite.pos[1] > item.pos[1]:
            self.ver_collide(sprite, item, by_gravity=False)
    
    def ver_collide(self, sprite, item, by_gravity: bool = True) -> None:
        sprite_pos: tuple[float, float] = sprite.pos
        if by_gravity:
            sprite_y: float = self.gravity_collide(item, sprite)
        else:
            sprite_y: float = self.jump_collide(item, sprite)
        sprite.pos = sprite_pos[0], sprite_y
    
    def gravity_collide(self, item, sprite) -> float:
        sprite_y: float = item.pos[1] - sprite.sizes[1] * 1.01
        sprite.gravity.grounded = True
        self.fix_jumper(sprite)
        return sprite_y
    
    def jump_collide(self, item, sprite) -> float:
        sprite_y: float = item.pos[1] + item.sizes[1]
        self.fix_jumper(sprite, down=False)
        return sprite_y
    
    @staticmethod
    def fix_jumper(sprite, down: bool = True) -> None:
        if hasattr(sprite, 'jump') and down:
            sprite.jump.jumped = False
            sprite.jump.ground = sprite.pos[1] + sprite.sizes[1]
        if hasattr(sprite, 'jump') and not down:
            sprite.jump.jumped = True
            sprite.gravity.grounded = False
    
    def __del__(self) -> None:
        pass


class MarioBlocks(SolidBlocks):
    """A class for controlling collisions with blocks from the mario game(block with interact method)"""
    def __init__(self) -> None:
        super().__init__()
       
    def do_collision(self, sprite,
                     limiter: float = 0,
                     hor_repulse: bool = False) -> None:
        self.fix_jumping(sprite)
        for item in self.tar:
            if sprite.rect.colliderect(item.rect) and not item.destroyed:
                self.correct_hor_collide(sprite, item, limiter, hor_repulse)
                self.ver_collider(sprite, item)

    def jump_collide(self, item, sprite) -> float:
        item.interact(sprite)
        sprite_y: float = super().jump_collide(item, sprite)
        return sprite_y
    
    def __del__(self) -> None:
        pass


class TransportPlatforms(MarioBlocks):
    """Control of sprite and vehicle interaction. The objects must implement the Transport interface"""
    def __init__(self) -> None:
        super().__init__()
        
    def do_collision(self, sprite,
                     limiter: float = 0,
                     hor_repulse: bool = False) -> None:
        self.fix_jumping(sprite)
        for item in self.tar:
            self.fix_ride(item, sprite)
            if sprite.rect.colliderect(item.rect) and not item.destroyed:
                self.correct_hor_collide(sprite, item, limiter, hor_repulse)
                self.ver_collider(sprite, item)
                
    @staticmethod
    def fix_ride(item, sprite) -> None:
        delta_x: float = abs(item.rect.centerx - sprite.rect.centerx)       
        delta_y: float = item.rect.centery - sprite.rect.centery
        k_x: float = item.sizes[0] * .6
        k_y: float = item.sizes[1] * .5 + sprite.sizes[1] * .6
        if (delta_x <= k_x) and ((delta_y > 0) and (abs(delta_y) <= k_y)):
            item.joy_ride(sprite)
 
    def joy_rides(self, sprite) -> None:
        for item in self.tar:
            if sprite.rect.colliderect(item.rect) and not item.destroyed:
                item.joy_ride(sprite)

    def __del__(self) -> None:
        pass


class SurpriseBlocks(SolidBlocks):
    def __init__(self) -> None:
        super().__init__()

    def jump_collide(self, item, sprite, collection) -> None:
        item.interact(sprite, collection)
        sprite_y: float = super().jump_collide(item, sprite)
        return sprite_y
  
    def ver_collide(self, sprite, item, collection, by_gravity: bool = True) -> None:
        sprite_pos: tuple[float, float] = sprite.pos
        if by_gravity:
            sprite_y: float = self.gravity_collide(item, sprite)
        else:
            sprite_y: float = self.jump_collide(item, sprite, collection)
        sprite.pos = sprite_pos[0], sprite_y
   
    def ver_collision(self, sprite, collection) -> None:
        for item in self.tar:
            if sprite.rect.colliderect(item.rect):
                self.ver_collider(sprite, item, collection)
    
    def ver_collider(self, sprite, item, collection) -> None:
        if (sprite.pos[1] < item.pos[1]) and not sprite.gravity.grounded:
            self.ver_collide(sprite, item, collection)
        if sprite.pos[1] > item.pos[1]:
            self.ver_collide(sprite, item, collection, by_gravity=False)
    
    def do_collision(self, sprite,
                     collection,
                     limiter: float = 0,
                     hor_repulse: bool = False) -> None:
        self.fix_jumping(sprite)
        for item in self.tar:
            if sprite.rect.colliderect(item.rect):
                self.correct_hor_collide(sprite, item, limiter, hor_repulse)
                self.ver_collider(sprite, item, collection)

    def __del__(self) -> None:
        pass
