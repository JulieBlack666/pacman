from GameObjects.BlueGhost import BlueGhost
from GameObjects.Food import Food
from GameObjects.GhostHomeDoor import GhostHomeDoor
from GameObjects.OrangeGhost import OrangeGhost
from GameObjects.Pacman import Pacman
from GameObjects.PinkGhost import PinkGhost
from GameObjects.RedGhost import RedGhost
from GameObjects.Wall import Wall


class Level:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.element_size = 0
        self. map = [[]]
        self.moving_objects = []

    def create(self, element_size):
        self.width = 21
        self.height = 22
        self.food_count = 0
        self.element_size = element_size
        self.map = [[None for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                if (y == 0 or x == 0 or y == self.height - 1 or x == self.width - 1) \
                        and y != 10 and y != 8 and y != 12:
                    self.map[y][x] = Wall()
                elif x == 10 and y < 4:
                    self.map[y][x] = Wall()
                elif (2 <= x <= 3 or 5 <= x <= 8 or 12 <= x <= 15 or 17 <= x <= 18) and 2 <= y <= 3:
                    self.map[y][x] = Wall()
                elif (x == 5 or x == 15) and 6 <= y <= 9 or x == 10 and 6 <= y <= 7:
                    self.map[y][x] = Wall()
                elif y == 5 and (2 <= x <= 3 or x == 5 or 7 <= x <= 13 or x == 15 or 17 <= x <= 18):
                    self.map[y][x] = Wall()
                elif y == 7 and (1 <= x <= 3 or 6 <= x <= 8 or 12 <= x <= 14 or 17 <= x <= 19):
                    self.map[y][x] = Wall()
                elif (y == 9 or y == 11 or y == 13) and (1 <= x <= 3 or 17 <= x <= 19):
                    self.map[y][x] = Wall()
                elif y == 9 and (7 <= x <= 9 or 11 <= x <= 13) or y == 10 and (x == 7 or x == 13)\
                        or y == 11 and 7 <= x <= 13:
                    self.map[y][x] = Wall()
                elif y == 9 and x == 10:
                    self.map[y][x] = GhostHomeDoor()
                elif (y == 8 or y == 12) and (x == 3 or x == 17):
                    self.map[y][x] = Wall()
                elif y == 13 and 7 <= x <= 13 or (x == 5 or x == 15) and 11 <= y <= 13:
                    self.map[y][x] = Wall()
                elif x == 10 and 14 <= y <= 15 or y == 15 and (2 <= x <= 3 or 5 <= x <= 8 or 12 <= x <= 15
                                                               or 17 <= x <= 18):
                    self.map[y][x] = Wall()
                elif y == 17 and (x == 1 or x == 19 or x == 3 or x == 17 or x == 5 or x == 15
                                  or 7 <= x <= 13) or y == 16 and (x == 3 or x == 17):
                    self.map[y][x] = Wall()
                elif y == 18 and (x == 5 or x == 10 or x == 15) or y == 19 and (2 <= x <= 8
                                                                                or x == 10 or 12 <= x <= 18):
                    self.map[y][x] = Wall()
                elif x == 1 and y == 3 or x == self.width - 2 and y == 3 or x == 1 and y == self.height - 6 \
                        or x == self.width - 2 and y == self.height - 6:
                    self.map[y][x] = Food(True)
                    self.food_count += 1
                elif not (y == 10 and 8 <= x <= 12 or y == 9 and x == 10 or (y == 8 or y == 12) and (0 <= x <= 2
                                                                                                     or 17 <= x <= 20)):
                    self.map[y][x] = Food(False)
                    self.food_count += 1
        self.moving_objects = [Pacman(10 * self.element_size, 16 * self.element_size),
                               RedGhost(10 * self.element_size, 8 * self.element_size),
                               PinkGhost(10 * self.element_size, 10 * self.element_size),
                               BlueGhost(9 * self.element_size, 10 * self.element_size),
                               OrangeGhost(11 * self.element_size, 10 * self.element_size)]
        self.red_ghost = self.moving_objects[1]
        return self
