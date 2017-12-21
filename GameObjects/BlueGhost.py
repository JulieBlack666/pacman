from GameObjects.Ghost import Ghost
from Point import Point
from Vector import Vector


class BlueGhost(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, Point(1, 0), 'ghost3.png')

    def move(self, game):
        point_before_pacman = game.player.location + game.player.current_direction.multiply(2 * game.element_size)
        vector = Vector(game.red_ghost.location, point_before_pacman)
        point_to_chase = vector.multiply(2).end
        self.move_to_point(game, point_to_chase, Point(15 * game.element_size, 19 * game.element_size))
