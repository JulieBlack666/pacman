from threading import Timer

from GameObjects import Ghost, GhostHomeDoor

from GameObjects.Wall import Wall
from Point import Point


class Pacman:
    def __init__(self, x, y):
        self.score = 0
        self.is_dead = False
        self.spawn_location = Point(x, y)
        self.location = self.spawn_location
        self.current_direction = Point(1, 0)
        self.next_direction = Point(0, 0)
        self.has_superpower = False
        self.should_scare = False
        self.power_counter = 0
        self.current_image_name = ''
        self.lives_count = 3
        self.add_images()

    def add_images(self):
        self.images_names_up = ['pacman_up1.png', 'pacman_up2.png', 'pacman_closed.png']
        self.images_names_down = ['pacman_down1.png', 'pacman_down2.png', 'pacman_closed.png']
        self.images_names_right = ['pacman_right1.png', 'pacman_right2.png', 'pacman_closed.png']
        self.images_names_left = ['pacman_left1.png', 'pacman_left2.png', 'pacman_closed.png']

    def respawn(self):
        self.current_direction = Point(0,0)
        Timer(1.0, self.spawn).start()

    def spawn(self):
        self.location = self.spawn_location
        self.is_dead = False

    def set_direction(self, dir):
        if self.current_direction == Point(0, 0) or self.current_direction + dir == Point(0,0):
            self.current_direction = dir
            self.next_direction = Point(0, 0)
        elif dir != self.current_direction:
            self.next_direction = dir

    def move(self, game):
        if self.power_counter > 0:
            self.power_counter -= 1
        else:
            self.has_superpower = False
        if self.next_direction != Point(0, 0) and self.can_turn(game.element_size) \
                and self.can_go(self.next_direction, game):
                self.current_direction = self.next_direction
                self.next_direction = Point(0, 0)
        if self.can_go(self.current_direction, game):
            self.location += self.current_direction
            self.location.put_in_borders((len(game.map[0]) - 1) * game.element_size,
                                         (len(game.map) - 1) * game.element_size)
        else:
            self.current_direction = Point(0, 0)
            self.next_direction = Point(0, 0)

    def check_collision(self, other):
        if isinstance(other, Ghost.Ghost) and not self.has_superpower and not other.is_dead and not self.is_dead:
            self.lives_count -= 1
            self.is_dead = True

    def give_power(self):
        self.has_superpower = True
        self.should_scare = True
        self.power_counter = 900

    def can_turn(self, size):
        return self.next_direction.x != 0 and self.location.y % size == 0 \
               or self.next_direction.y != 0 and self.location.x % size == 0

    def can_go(self, direction, game):
        next_coords = self.location + direction
        next_coords.put_in_borders((len(game.map[0]) - 1) * game.element_size, (len(game.map) - 1) * game.element_size)
        return next_coords.is_free_to_go(direction, game, GhostHomeDoor.GhostHomeDoor)

    def get_image_name(self):
        if self.current_direction == Point(0, 1):
            self.current_image_name = self.images_names_down[(self.location.y // 30) % 3]
        elif self.current_direction == Point(0, -1):
            self.current_image_name = self.images_names_up[(self.location.y // 30) % 3]
        elif self.current_direction == Point(1, 0):
            self.current_image_name = self.images_names_right[(self.location.x // 30) % 3]
        elif self.current_direction == Point(-1, 0):
            self.current_image_name = self.images_names_left[(self.location.x // 30) % 3]
        return self.current_image_name
