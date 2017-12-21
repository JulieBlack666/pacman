from Point import Point


class Vector:
    def __init__(self, point_start, point_end):
        self.start = point_start
        self.end = point_end
        self.length = int(((point_end.x - point_start.x)**2 + (point_end.y - point_start.y)**2)**1/2)

    def multiply(self, number):
        start = self.start
        if self.length != 0:
            cos = (self.end.y - self.start.y) / self.length
            sin = (self.end.x - self.start.x) / self.length
            end_x = int(self.length * number * sin)
            end_y = int(self.length * number * cos)
            return Vector(start, Point(end_x, end_y))
        else:
            return self
