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
        # self.vision(self.fruits)
        self.state = self.get_state()
        return self.state

    def step(self, action=None):
        """Advances the game state by one step based on the given action."""
        reward = 0
        if action is not None:
            self.snake.set_direction(action)
            print(f"{action}\n")
        self.snake.move()
        # self.vision(self.fruits)
        reward += self.check_wall_collision()
        reward += self.check_self_collision()
        reward += self.check_fruit_collision()
        if not self.game_over:
            self.state = self.get_state()
        self.move_count += 1
        return self.state, reward, self.game_over

# def get_state(self):
#     head_x, head_y = self.snake.body[0]
#     vision_grid = self.vision(self.fruits)
#     up_string = "".join(vision_grid[i][head_x + 1]
#                         for i in range(head_y + 1))
#     down_string = "".join(vision_grid[i][head_x + 1]
#                           for i in range(head_y + 2, len(vision_grid)))
#     left_string = "".join(vision_grid[head_y + 1][i]
#                           for i in range(head_x + 1))
#     right_string = "".join(vision_grid[head_y + 1][i]
#                            for i in range(head_x + 2, len(vision_grid[0])))

#     state = (
#             up_string,
#             down_string,
#             left_string,
#             right_string,
#             self.snake.direction
#         )
#     print(f"State: {state}\n")
#     return state

    def get_state(self):
        head_x, head_y = self.snake.body[0]
        vision_grid = self.vision(self.fruits)
        up_string = "".join(vision_grid[i][head_x + 1]
                            for i in range(head_y + 1))
        down_string = "".join(vision_grid[i][head_x + 1]
                              for i in range(head_y + 2, len(vision_grid)))
        left_string = "".join(vision_grid[head_y + 1][i]
                              for i in range(head_x + 1))
        right_string = "".join(vision_grid[head_y + 1][i]
                               for i in range(head_x + 2, len(vision_grid[0])))

        def is_dangerous(char: str) -> bool:
            """Determines if a character in the vision grid
            represents a danger to the snake."""
            return (
                char == 'W' or
                char == 'S' or
                (char == 'R' and len(self.snake.body) <= 2)
            )

        # Immediate Danger in each direction
        danger = (
            is_dangerous(up_string[0]),
            is_dangerous(down_string[0]),
            is_dangerous(left_string[0]),
            is_dangerous(right_string[0]),
        )

        # First object seen on the path
        def scan(string: str) -> str:
            """Iterates through the squares in order and returns
            whatever is seen first: 'W', 'G', 'R'.

            The snake's body is treated as a wall
            to minimize the number of states.
            """
            for char in string:
                if is_dangerous(char):
                    return 'W'  # Wall, Body or Dangerous Red Apple
                if char == 'G' or char == 'R':
                    return char
            return 'W'

        up = scan(up_string)
        down = scan(down_string)
        left = scan(left_string)
        right = scan(right_string)

        return (
            danger,
            self.snake.direction,
            up, down, right, left,  # 'W' | 'G' | 'R'
        )

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
        reward = 0
        for fruit in self.fruits:
            if fruit.position == (head_x, head_y):
                self.fruits.remove(fruit)
                if fruit.color == c.GREEN:
                    self.snake.grow()
                    self.green_apples_eaten += 1
                    reward += c.GREEN_REWARD
                else:
                    self.red_apples_eaten += 1
                    self.snake.shrink()
                    if self.snake.get_size() <= 3:
                        reward += c.RED_SMALL_SNAKE_REWARD
                    else:
                        reward += c.RED_REWARD
                    if self.snake.get_size() <= 0:
                        self.game_over = True
                        reward += c.DEATH_REWARD
                self.spawn_fruit(c.GREEN if fruit.color == c.GREEN else c.RED)
                return reward
        return reward

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
            return c.DEATH_REWARD
        return 0

    def check_self_collision(self):
        """Checks if the snake's head has collided with its own body."""
        head = self.snake.body[0]
        if head in self.snake.body[1:]:
            self.game_over = True
            return c.DEATH_REWARD
        return 0

    def vision(self, fruits):
        """Generates a vision grid for the snake,
        showing the relative positions.
        """
        head_x, head_y = self.snake.body[0]
        body_positions = set(self.snake.body[1:])
        fruit_map = {tuple(f.position): f for f in fruits}

        def cell_symbol(x, y):
            if (x, y) == (head_x, head_y):
                return "H"
            if (x, y) in body_positions:
                return "S"
            if fruit := fruit_map.get((x, y)):
                return "G" if fruit.color == c.GREEN else "R"
            return "O"

        # Empty Grid with Walls (size + 2 for borders)
        size = self.config.nb_cells + 2
        vision_data = [[" "] * size for _ in range(size)]

        # Walls (W) on the cross borders
        vision_data[0][head_x + 1] = "W"
        vision_data[size - 1][head_x + 1] = "W"
        vision_data[head_y + 1][0] = "W"
        vision_data[head_y + 1][size - 1] = "W"

        # Vertical line (x == head_x)
        for y in range(self.config.nb_cells):
            vision_data[y + 1][head_x + 1] = cell_symbol(head_x, y)

        # Horizontal line (y == head_y)
        for x in range(self.config.nb_cells):
            vision_data[head_y + 1][x + 1] = cell_symbol(x, head_y)

        for row in vision_data:
            print("".join(row))
        print()
        return vision_data
