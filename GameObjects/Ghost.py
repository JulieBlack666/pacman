import random
from threading import Timer
from GameObjects import Pacman, Wall
from Point import Point


class Ghost:
    def __init__(self, x, y, direction, image_name):
        self.location = Point(x, y)
        self.image_name = image_name
        self.is_dead = False
        self.mode = 'scatter'
        self.home = Point(10 * 32, 10 * 32)
        self.initial_direction = direction
        self.spawn_location = self.location
        self.current_possible_directions = [direction]
        self.directions = [Point(0, 1), Point(0, -1), Point(1, 0), Point(-1, 0)]
        self.direction = direction
        self.timers = []
        self.start_timers()
        self.mode_changed = False

    def start_timers(self):
        mode_changing = {7: 'chase', 27: 'scatter', 34: 'chase', 54: 'scatter', 59: 'chase', 79: 'scatter',
                         84: 'chase'}
        for time, mode in mode_changing.items():
            t = Timer(time, self.change_mode, args=[mode])
            self.timers.append(t)
            t.start()

    def stop_timers(self):
        for timer in self.timers:
            timer.cancel()

    def choose_direction(self, point):
        next_direction = self.current_possible_directions[0]
        distance = (self.location + next_direction).distance(point)
        for dir in self.current_possible_directions:
            new_distance = (self.location + dir).distance(point)
            if new_distance < distance:
                distance = new_distance
                next_direction = dir
        self.direction = next_direction

    def is_at_crossroads(self, game):
        possible_directions = []
        for direction in self.directions:
            if (self.may_turn(game.element_size, direction) and self.direction + direction != Point(0, 0)
                 or direction == self.direction) and self.can_go(direction, game):
                possible_directions.append(direction)
        if len(possible_directions) > 1 or len(possible_directions) > 0 and not self.can_go(self.direction, game):
            self.current_possible_directions = possible_directions
            return True
        return False

    def move_to_point(self, game, point_to_chase, point_to_scatter):
        if self.mode_changed:
            new_dir = self.direction.multiply(-1)
            if (self.location + new_dir).is_free_to_go(new_dir, game):
                self.direction = new_dir
            else:
                self.direction = self.current_possible_directions[-1]
            self.mode_changed = False
        elif self.is_at_crossroads(game):
            point_to_go = self.location
            if self.is_dead:
                if self.location == self.home:
                    self.is_dead = False
                else:
                    point_to_go = self.home
                    self.mode = 'scatter'
            elif self.mode == 'chase':
                point_to_go = point_to_chase
            elif self.mode == 'scatter':
                point_to_go = point_to_scatter
            if self.mode == 'frighten':
                self.set_random_direction()
            elif self.location == self.home:
                self.set_direction(Point(0, -1))
            else:
                self.choose_direction(point_to_go)
        self.location += self.direction
        self.location.put_in_borders((len(game.map[0]) - 1) * game.element_size,
                                     (len(game.map) - 1) * game.element_size)

    def can_go(self, direction, game):
        next_coords = self.location + direction
        next_coords.put_in_borders((len(game.map[0]) - 1) * game.element_size,
                                   (len(game.map) - 1) * game.element_size)
        return next_coords.is_free_to_go(direction, game)

    def may_turn(self, size, direction):
        return direction.x != 0 and self.location.y % size == 0 or direction.y != 0 and self.location.x % size == 0

    def check_collision(self, other):
        if isinstance(other, Pacman.Pacman) and other.has_superpower and not self.is_dead:
            other.score += 200
            self.is_dead = True
            self.mode = 'chase'

    def change_mode(self, mode):
        if mode == 'frighten':
            self.stop_timers()
        if self.mode == 'frighten':
            self.start_timers()
        self.mode = mode
        self.mode_changed = True

    def set_random_direction(self):
        self.direction = self.current_possible_directions[random.randint(0, len(self.current_possible_directions)) - 1]

    def respawn(self):
        self.direction = Point(0, 0)
        Timer(1.0, self.spawn).start()

    def spawn(self):
        self.location = self.spawn_location
        self.is_dead = False
        self.direction = self.initial_direction
        self.mode = 'chase'

    def set_direction(self, dir):
        self.direction = dir

    def get_image_name(self):
        return 'scared_ghost.png' if self.mode == 'frighten' else 'dead_ghost.png' if self.is_dead else self.image_name
