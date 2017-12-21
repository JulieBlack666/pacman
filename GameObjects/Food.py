class Food:
    def __init__(self, gives_power):
        self.gives_power = gives_power
        self.image_name = 'big_food.png' if gives_power else 'food.png'

    def be_eaten(self, pacman):
        if self.gives_power:
            pacman.give_power()
            pacman.score += 50
        else:
            pacman.score += 10
