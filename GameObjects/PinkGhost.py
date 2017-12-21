from GameObjects.Ghost import Ghost
from Point import Point


class PinkGhost(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, Point(0, -1), 'ghost2.png')

    def move(self, game):
        point_to_chase = game.player.location + game.player.current_direction.multiply(4 * game.element_size)
        self.move_to_point(game, point_to_chase, Point(2 * game.element_size, 2 * game.element_size))