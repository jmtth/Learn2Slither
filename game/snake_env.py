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

    def step(self, action=None):
        if action is not None:
            self.snake.set_direction(action)
        self.snake.move()
        self.check_wall_collision()
        self.check_self_collision()
        self.check_fruit_collision()
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

    def check_fruit_collision(self):
        head_x, head_y = self.snake.body[0]
        for fruit in self.fruits:
            if fruit.position == (head_x, head_y):
                self.fruits.remove(fruit)
                if fruit.color == c.GREEN:
                    self.snake.grow()
                    self.score += 1
                else:
                    self.score += -1
                    self.snake.shrink()
                    if self.snake.get_size() <= 0:
                        self.game_over = True
                        break
                self.spawn_fruit(c.GREEN if fruit.color == c.GREEN else c.RED)
                break

    def check_wall_collision(self):
        head_x, head_y = self.snake.body[0]
        if head_x < 0 or head_x >= self.config.nb_cells or head_y < 0 or head_y >= self.config.nb_cells:
            self.game_over = True

    def check_self_collision(self):
        head = self.snake.body[0]
        if head in self.snake.body[1:]:
            self.game_over = True
