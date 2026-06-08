import random

from game.apple import Apple
from game.snake import Snake
import const as c


class SnakeEnv:
    """Represents the game environment for the Snake game."""
    def __init__(self, config):
        self.config = config
        self.reset()

    def reset(self):
        """Resets the game environment to the initial state."""
        self.snake = Snake(self.config)
        self.fruits = []
        self.green_apples_eaten = 0
        self.red_apples_eaten = 0
        self.move_count = 0
        self.game_over = False
        self.paused = False
        for i in range(self.config.nb_apples):
            if i == 0:
                self.spawn_fruit(c.RED)
            else:
                self.spawn_fruit(c.GREEN)

    def step(self, action=None):
        """Advances the game state by one step based on the given action."""
        if action is not None:
            self.snake.set_direction(action)
        self.snake.move()
        self.check_wall_collision()
        self.check_self_collision()
        self.check_fruit_collision()
        self.move_count += 1

    def get_state(self):
        pass

    def spawn_fruit(self, color):
        """Spawns a new fruit of the given color at a random position
        not occupied by the snake or other fruits.
        """
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
        """ Checks if the snake's head has collided with any fruit
        and updates the game state accordingly.
        """
        head_x, head_y = self.snake.body[0]
        for fruit in self.fruits:
            if fruit.position == (head_x, head_y):
                self.fruits.remove(fruit)
                if fruit.color == c.GREEN:
                    self.snake.grow()
                    self.green_apples_eaten += 1
                else:
                    self.red_apples_eaten += 1
                    self.snake.shrink()
                    if self.snake.get_size() <= 0:
                        self.game_over = True
                        break
                self.spawn_fruit(c.GREEN if fruit.color == c.GREEN else c.RED)
                break

    def check_wall_collision(self):
        """Checks if the snake's head has collided
        with the walls of the game area.
        """
        head_x, head_y = self.snake.body[0]
        if (
            head_x < 0
            or head_x >= self.config.nb_cells
            or head_y < 0 or head_y >= self.config.nb_cells
        ):
            self.game_over = True

    def check_self_collision(self):
        """Checks if the snake's head has collided with its own body."""
        head = self.snake.body[0]
        if head in self.snake.body[1:]:
            self.game_over = True
