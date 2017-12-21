import unittest
from Game import Game
from GameObjects import Pacman
from GameObjects.Food import Food
from GameObjects.Ghost import Ghost
from GameObjects.RedGhost import RedGhost
from GameObjects.Wall import Wall
from Level import Level
from Point import Point


class Tests(unittest.TestCase):
    def create_test_game(self, width, height, static_objects, moving_objects):
        level = Level()
        level.width = width
        level.height = height
        level.element_size = 1
        level.red_ghost = None
        level.map = [[None for _ in range(width)] for _ in range(height)]
        for obj, coords in static_objects.items():
            level.map[coords.y][coords.x] = obj
        level.moving_objects = moving_objects
        return Game(level)

    def test_pacman_moves_up(self):
        game = self.create_test_game(4, 4, {}, [Pacman.Pacman(2, 2)])
        game.player.set_direction(Point(0, -1))
        game.update()
        self.assertEqual(game.player.location, Point (2,1))

    def test_pacman_moves_right(self):
        game = self.create_test_game(5, 4, {}, [Pacman.Pacman(2, 2)])
        game.player.set_direction(Point(1, 0))
        game.update()
        self.assertEqual(game.player.location, Point(3, 2))

    def test_pacman_moves_few_times(self):
        game = self.create_test_game(4, 4, {}, [Pacman.Pacman(2,3)])
        game.player.set_direction(Point(0, -1))
        game.update()
        game.update()
        game.update()
        self.assertEqual(game.player.location, Point (2,0))

    def test_pacman_doesnt_move_in_wall(self):
        game = self.create_test_game(5, 4, {Wall(): Point(3, 2)}, [Pacman.Pacman(2, 2)])
        game.player.set_direction(Point(1, 0))
        game.update()
        self.assertEqual(game.player.location, Point(2, 2))

    def test_pacman_two_directions(self):
        game = self.create_test_game(8, 8, {Wall(): Point(2, 1), Wall(): Point(3, 1)}, [Pacman.Pacman(2, 2)])
        game.player.set_direction(Point(1, 0))
        game.player.set_direction(Point(0, -1))
        game.update()
        self.assertEqual(game.player.location, Point(3, 2))
        game.update()
        game.update()
        self.assertEqual(game.player.location, Point(4, 1))

    def test_pacman_eats_usual_food(self):
        game = self.create_test_game(5, 4, {Food(False): Point(3, 2)}, [Pacman.Pacman(2, 2)])
        game.player.set_direction(Point(1, 0))
        game.update()
        self.assertEqual(game.player.score, 10)
        self.assertEqual(game.map[2][3], None)
        self.assertFalse(game.player.has_superpower)

    def test_pacman_eats_big_food(self):
        game = self.create_test_game(5, 4, {Food(True): Point(3, 2)}, [Pacman.Pacman(2, 2)])
        game.player.set_direction(Point(1, 0))
        game.update()
        self.assertEqual(game.player.score, 50)
        self.assertEqual(game.map[2][3], None)
        self.assertTrue(game.player.has_superpower)

    def test_red_ghost_moves_left(self):
        ghost = RedGhost(1, 2)
        game = self.create_test_game(5, 5, {}, [Pacman.Pacman(3, 2), ghost])
        game.player.set_direction(Point(0, 0))
        ghost.mode = 'chase'
        ghost.stop_timers()
        game.update()
        self.assertEqual(ghost.location, Point(0, 2))

