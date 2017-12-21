from GameObjects.Ghost import Ghost
from Point import Point


class OrangeGhost(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, Point(-1, 0), 'ghost4.png')

    def move(self, game):
        point_to_scatter = Point(5 * game.element_size, 19 * game.element_size)
        point_to_chase = game.player.location if self.location.distance(game.player.location) < 8 * game.element_size \
            else point_to_scatter
        self.move_to_point(game, point_to_chase, point_to_scatter)