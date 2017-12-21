from GameObjects.Wall import Wall


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def multiply(self, other):
        return Point(other * self.x, other * self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def distance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**(1/2)

    def is_close_to(self, other, needed_distance):
        return abs(self.x - other.x) <= needed_distance and abs(self.y - other.y) <= needed_distance

    def is_free_to_go(self, direction, game, item_to_check = None):
        x = self.x // game.element_size if direction.x <= 0 \
            else (self.x + game.element_size - 1) // game.element_size
        y = self.y // game.element_size if direction.y <= 0 \
            else (self.y + game.element_size - 1) // game.element_size
        if item_to_check is not None and isinstance(game.map[y][x], item_to_check):
            return False
        return not isinstance(game.map[y][x], Wall)

    def put_in_borders(self, width, height):
        if self.x < 0 or self.x >= width:
            self.x = (self.x % width + width) % width
        if self.y < 0 or self.y >= height:
            self.y = (self.y % height + height) % height