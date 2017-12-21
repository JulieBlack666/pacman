class Game:
    def __init__(self, level):
        self.width = level.width
        self.height = level.height
        self.map = level.map
        self.food_count = level.food_count
        self.won = False
        self.moving_objects = level.moving_objects
        self.element_size = level.element_size
        self.player = self.moving_objects[0]
        self.red_ghost = level.red_ghost
        self.game_is_over = False

    def update(self):
        for object in self.moving_objects:
            object.move(self)
        x = self.player.location.x // self.element_size
        y = self.player.location.y // self.element_size
        if self.map[y][x] is not None:
            self.map[y][x].be_eaten(self.player)
            self.map[y][x] = None
            self.food_count -= 1
        self.check_collisions_with_ghosts()
        self.player.should_scare = False
        if self.player.lives_count == 0:
            self.game_is_over = True
            for ghost in self.moving_objects[1:]:
                ghost.stop_timers()
        elif self.player.is_dead:
            self.respawn_all()
        elif self.food_count <= 0:
            self.won = True


    def check_collisions_with_ghosts(self):
        for ghost in self.moving_objects[1:]:
            if self.player.location.is_close_to(ghost.location, self.element_size / 2):
                self.player.check_collision(ghost)
                ghost.check_collision(self.player)
            if self.player.should_scare:
                if ghost.mode != 'frighten' and not ghost.is_dead:
                    ghost.change_mode('frighten')
            elif ghost.mode == 'frighten' and not self.player.has_superpower:
                ghost.change_mode('scatter')

    def respawn_all(self):
        for obj in self.moving_objects:
            obj.respawn()
