import random

from game.apple import Apple
from game.snake import Snake
import const as c


class SnakeEnv:

    def __init__(self, config):
        self.config = config
        self.reset()

    def reset(self):
        self.snake = Snake(self.config)
        self.fruits = []  # Initialize fruits list
        self.score = 0
        self.game_over = False
        self.paused = False
        for i in range(self.config.nb_apples):
            if i == 0:
                self.spawn_fruit(c.RED)
            else:
                self.spawn_fruit(c.GREEN)

    def step(self, action):
        pass

    def get_state(self):
        pass

    def spawn_fruit(self, color):
        occupied_positions = {
                tuple(pos)
                for pos in self.snake.body
            }
        occupied_positions.update(
                tuple(fruit.position)
                for fruit in self.fruits
            )
        while True:
            position = (
                random.randrange(self.config.nb_cells),
                random.randrange(self.config.nb_cells)
            )
            if position not in occupied_positions:
                break

        self.fruits.append(Apple(color, position))

    def check_collision(self):
        pass

