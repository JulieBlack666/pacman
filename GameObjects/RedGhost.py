from GameObjects import Ghost
from Point import Point


class RedGhost(Ghost.Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, Point(-1, 0), 'ghost1.png')

    def move(self, game):
        self.move_to_point(game, game.player.location, Point(17 * game.element_size, 2 * game.element_size))
