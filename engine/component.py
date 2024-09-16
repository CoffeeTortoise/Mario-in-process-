from engine.constants import DrawBounds, UpdateBounds
from engine.tools import Timer


class BoundChecker:
    def __init__(self,
                 x: tuple[float, float] | None = None,
                 y: tuple[float, float] | None = None,
                 in_bound: bool = True) -> None:
        if x is None:
            self.x: tuple[float, float] = 0, 0
        else:
            self.x: tuple[float, float] = x
        if y is None:
            self.y: tuple[float, float] = 0, 0
        else:
            self.y: tuple[float, float] = y
        self.in_bound: bool = in_bound
    
    def check_bound(self, pos) -> None:
        if self.check_x(pos[0]) and self.check_y(pos[1]):
            self.in_bound = True
        else:
            self.in_bound = False
    
    def check_x(self, pos_x: float) -> bool:
        return (pos_x >= self.x[0]) and (pos_x <= self.x[1])
    
    def check_y(self, pos_y: float) -> bool:
        return (pos_y >= self.y[0]) and (pos_y <= self.y[1])
    
    def __del__(self) -> None:
        pass
        
    
class Drawable(BoundChecker):
    def __init__(self,
                 x: tuple[float, float] | None = None,
                 y: tuple[float, float] | None = None,
                 in_bound: bool = True) -> None:
        super().__init__(x, y, in_bound)
        draw_border: DrawBounds = DrawBounds()
        self.x: tuple[float, float] = draw_border.bound_x
        self.y: tuple[float, float] = draw_border.bound_y
    
    def __del__(self) -> None:
        pass


class Updatable(BoundChecker):
    def __init__(self,
                 x: tuple[float, float] | None = None,
                 y: tuple[float, float] | None = None,
                 in_bound: bool = True) -> None:
        super().__init__(x, y, in_bound)
        update_bounds: UpdateBounds = UpdateBounds()
        self.x: tuple[float, float] = update_bounds.bound_x
        self.y: tuple[float, float] = update_bounds.bound_y
    
    def __del__(self) -> None:
        pass


class Delta:
    """A class for obtaining value of a quantity in an infinitesimal period of time"""
    def __init__(self, value: float, max_value: float) -> None:
        self.value: float = value
        self.max_value: float = max_value * .75
        self.limiter: float = max_value
        self.__timer: Timer = Timer()

    def get_current(self) -> float:
        value: float = self.get_delta()
        fixed_value: float = self.fix_value(value)
        return fixed_value
    
    def get_delta(self) -> float:
        elapsed_time: float = self.__timer.restart()
        return self.value * elapsed_time
    
    def limit_value(self, value: float) -> float:
        if value > self.max_value:
            return self.max_value
        else:
            return value
    
    def fix_value(self, value: float) -> float:
        if (value > self.max_value) or (value == 0):
            return self.max_value
        else:
            return value
    
    def __del__(self) -> None:
        pass


class Speed(Delta):
    """A class for storing and controlling speed. Based on class Delta"""
    def __init__(self, value: float, max_value: float,
                 right: bool = True,
                 down: bool = True) -> None:
        super().__init__(value, max_value)
        self.right: bool = right
        self.down: bool = down
    
    def move_x(self, rect, to_right = True) -> None:
        self.move(rect, to_right)
    
    def move_y(self, rect, down = True) -> None:
        self.move(rect, down, fly=True)

    def get_shift(self, positive: bool = True) -> float:
        dd: float = self.get_speed()
        if (dd < 0) and positive:
            dd *= -1
        if (dd > 0) and not positive:
            dd *= -1
        return dd
    
    def move(self, rect, positive: bool = True, fly: bool = False) -> None:
        shift: float = self.get_shift(positive)
        self.shift_rect(rect, shift, positive, fly)
    
    def get_speed(self) -> float:
        speed: float = self.get_delta()
        fixed_speed: float = self.fix_value(speed)
        return fixed_speed
    
    def shift_rect(self, rect, delta: float, positive: bool = True, fly: bool = False) -> None:
        self.down = not fly
        if not fly:
            self.right = positive
            rect.move_ip(delta, 0)
        else:
            self.down = positive
            rect.move_ip(0, delta)
    
    def __del__(self) -> None:
        pass


class Gravity(Delta):
    """A class for storing and controlling gravity. Based on class Delta"""
    def __init__(self, value: float, 
                 max_value: float,
                 grounded: bool = False,
                 controlled: bool = False,
                 time_control: float = .16) -> None:
        super().__init__(value, max_value)
        self.__timer_grounded: Timer = Timer()
        self.time_control: float = time_control
        self.controlled: bool = controlled
        self.grounded: bool = grounded
    
    def apply_gravity(self, rect) -> None:
        if self.controlled:
            self.control_grounded()
        gravity: float = self.get_gravity()
        rect.move_ip(0, gravity)
    
    def control_grounded(self) -> None:
        time: float = self.__timer_grounded.get_time()
        if time >= self.time_control:
            self.grounded = False
            self.__timer_grounded.restart()
    
    def get_gravity(self) -> float:
        if self.grounded:
            return 0
        else:
            gravity: float = self.get_delta()
            fixed_gravity: float = self.fix_value(gravity)
            return fixed_gravity
    
    def __del__(self) -> None:
        pass


class Jump(Delta):
    def __init__(self, value: float, 
                 max_value: float,
                 ground: float,
                 height: float,
                 jumped: bool = False) -> None:
        super().__init__(value, max_value)
        self.ground: float = ground
        self.height: float = height
        self.jumped: bool = jumped
        self.in_jumping: bool = not jumped
    
    def jumping(self, rect) -> None:
        if not self.jumped:
            self.in_jumping = True
            jump: float = self.get_jump()
            rect.move_ip(0, jump)
            self.limit_jump(rect)
    
    def get_jump(self) -> float:
        if self.jumped:
            return 0
        else:
            jump: float = self.get_delta()
            fixed_jump: float = self.fix_value(jump)
            return fixed_jump
    
    def limit_jump(self, rect) -> None:
        height: float = abs(rect.top - self.ground)
        if height >= self.height:
            rect.top = self.ground - self.height
            self.stop_jumping()
    
    def stop_jumping(self) -> None:
        self.in_jumping = False
        self.jumped = True
    
    def __del__(self) -> None:
        pass


class HP:
    def __init__(self, health: float,
                 max_health: float) -> None:
        self.__health: float = health
        self.__max_health: float = max_health
    
    def increase_health(self, value: float) -> None:
        self.__health += value
        if self.__health >= self.__max_health:
            self.__max_health = self.__health
    
    def decrease_health(self, value: float) -> None:
        self.__health -= value
        if self.__health < 0:
            self.__health = 0
            
    @property
    def health(self) -> float:
        return self.__health

    @property
    def max_health(self) -> float:
        return self.__max_health
    
    @property
    def relative_health(self) -> float:
        return self.__health / self.__max_health
    
    def __del__(self) -> None:
        pass
