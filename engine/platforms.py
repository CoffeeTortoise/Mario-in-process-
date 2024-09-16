from engine.motions import Circle, Rotation, Patrol, Parabola
from engine.interfaces import Transport
from engine.block import MarioBlock


class RotatingPlatform(MarioBlock):
    """Right means clockwise"""
    def __init__(self, image,
                 brick_sound,
                 breakblock_sound,
                 sizes: tuple[float, float],
                 pos: tuple[float, float],
                 moments: int = 12,
                 speed: float = .15,
                 stop_rotation: bool = False,
                 destructible: bool = False,
                 in_activity: bool = True,
                 destroyed: bool = False,
                 on_screen: bool = True,
                 static: bool = False,
                 right: bool = True,
                 phys: bool = False) -> None:
        super().__init__(image, brick_sound, breakblock_sound, sizes, pos, destructible,
                         in_activity, destroyed, on_screen, static, right, phys)
        self.stop_rotation: bool = stop_rotation
        self.right_rotation: Rotation = Rotation(image, sizes, pos, moments, speed)
        self.left_rotation: Rotation = Rotation(image, sizes, pos, moments, speed, clockwise=False)

    def change_image(self) -> None:
        if not self.stop_rotation:
            self.rotate_image()
        else:
            self.image = self.picture.get_image()
            self.rect = self.image.get_rect()
            self.rect.center = self.right_rotation.pos

    def rotate_image(self) -> None:
        if self.right:
            self.image, self.rect = self.right_rotation.rotate()
        else:
            self.image, self.rect = self.left_rotation.rotate()

    def pure_resize(self, sizes: tuple[float, float]) -> None:
        super().pure_resize(sizes)
        self.right_rotation.total_resize(sizes)
        self.left_rotation.total_resize(sizes)

    def shift(self, dx: float = 0, dy: float = 0) -> None:
        super().shift(dx, dy)
        self.right_rotation.shift_center(dx, dy)
        self.left_rotation.shift_center(dx, dy)

    def __del__(self) -> None:
        pass


class ParabolaPlatform(MarioBlock, Transport):
    """Give argument fly_angle in degrees"""
    def __init__(self, image,
                 brick_sound,
                 breakblock_sound,
                 speed: float,
                 max_speed: float,
                 fly_angle: float,
                 sizes: tuple[float, float],
                 pos: tuple[float, float],
                 destructible: bool = False,
                 in_activity: bool = True,
                 destroyed: bool = False,
                 on_screen: bool = True,
                 static: bool = False,
                 right: bool = True,
                 down: bool = True,
                 phys: bool = False) -> None:
        MarioBlock.__init__(self, image, brick_sound, breakblock_sound, sizes, pos, destructible,
                             in_activity, destroyed, on_screen, static, right, phys)
        self.parabola_motion: Parabola = Parabola(speed, max_speed, fly_angle, right, down)
        self.offset: tuple[float, float] = 0, 0
    
    def main_update(self, pos: tuple[float, float]) -> None:
        super().main_update(pos)
        self.offset = self.parabola_motion.move_rect(self.rect)
    
    def sync_right(self) -> None:
        super().sync_right()
        self.parabola_motion.right = self.right
    
    def joy_ride(self, target) -> None:
        target.rect.move_ip(self.offset[0], self.offset[1])
    
    def __del__(self) -> None:
        pass


class CircleMovePlatform(MarioBlock, Transport):
    def __init__(self, image,
                 brick_sound,
                 breakblock_sound,
                 speed: float, 
                 max_speed: float,
                 radius: float, 
                 center: tuple[float, float],
                 sizes: tuple[float, float],
                 pos: tuple[float, float],
                 initial_angle: float = 0,
                 destructible: bool = False,
                 in_activity: bool = True,
                 destroyed: bool = False,
                 clockwise: bool = True,
                 on_screen: bool = True,
                 static: bool = False,
                 right: bool = True,
                 phys: bool = False) -> None:
        MarioBlock.__init__(self, image, brick_sound, breakblock_sound, sizes, pos, destructible,
                             in_activity, destroyed, on_screen, static, right, phys)
        self.circle_motion: Circle = Circle(speed, max_speed, radius,
                                            center, initial_angle, clockwise)
        self.offset: tuple[float, float] = 0, 0    #Can be used with target in interactive method

    def main_update(self, pos: tuple[float, float]) -> None:
        super().main_update(pos)
        self.offset = self.circle_motion.move_rect(self.rect)

    def shift(self, dx: float = 0, dy: float = 0) -> None:
        super().shift(dx, dy)
        self.circle_motion.shift_center(dx, dy)

    def joy_ride(self, target) -> None:
        target.rect.move_ip(self.offset[0], self.offset[1])

    def __del__(self) -> None:
        pass


class BoatPlatform(MarioBlock, Transport):
    """A platform moving left and right. The initial coordinate of the movement coincides with
    the position. length means the length of the movement"""
    def __init__(self, image,
                 brick_sound,
                 breakblock_sound,
                 speed: float,
                 length: float,
                 max_speed: float,
                 sizes: tuple[float, float],
                 pos: tuple[float, float],
                 destructible: bool = False,
                 in_activity: bool = True,
                 destroyed: bool = False,
                 on_screen: bool = True,
                 static: bool = False,
                 right: bool = True,
                 phys: bool = False) -> None:
        MarioBlock.__init__(self, image, brick_sound, breakblock_sound, sizes, pos, destructible,
                             in_activity, destroyed, on_screen, static, right, phys)
        self.patrol_x: Patrol = Patrol(speed, max_speed, length, pos[0], vertical=False)
        self.offset_x: float = 0    #offset x for joy riders

    def main_update(self, pos: tuple[float, float]) -> None:
        super().main_update(pos)
        self.offset_x = self.patrol_x.move_rect(self.rect)

    def shift(self, dx: float = 0, dy: float = 0) -> None:
        super().shift(dx, dy)
        self.patrol_x.shift_patrol(dx, dy)

    def joy_ride(self, target) -> None:
        target.rect.move_ip(self.offset_x, 0)

    def __del__(self) -> None:
        pass


class LiftPlatform(MarioBlock, Transport):
    """A platform moving left and right. The initial coordinate of the movement coincides with
    the position. length means the length of the movement"""
    def __init__(self, image,
                 brick_sound,
                 breakblock_sound,
                 speed: float,
                 length: float,
                 max_speed: float,
                 sizes: tuple[float, float],
                 pos: tuple[float, float],
                 destructible: bool = False,
                 in_activity: bool = True,
                 destroyed: bool = False,
                 on_screen: bool = True,
                 static: bool = False,
                 right: bool = True,
                 phys: bool = False) -> None:
        MarioBlock.__init__(self, image, brick_sound, breakblock_sound, sizes, pos, destructible,
                             in_activity, destroyed, on_screen, static, right, phys)
        self.patrol_y: Patrol = Patrol(speed, max_speed, length, pos[1], vertical=True)
        self.offset_y: float = 0    #offset y for joy riders

    def main_update(self, pos: tuple[float, float]) -> None:
        super().main_update(pos)
        self.offset_y = self.patrol_y.move_rect(self.rect)

    def shift(self, dx: float = 0, dy: float = 0) -> None:
        super().shift(dx, dy)
        self.patrol_y.shift_patrol(dx, dy)

    def joy_ride(self, target) -> None:
        target.rect.move_ip(0, self.offset_y)

    def __del__(self) -> None:
        pass
