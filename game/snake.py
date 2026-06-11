import random
from config import GameConfig


class Snake:
    """Represents the snake in the game."""
    def __init__(self, config: GameConfig):
        self.body = []
        self.direction = (-1, 0)  # Initial direction: moving right
        self.size = config.initial_size
        self.nb_cells = config.nb_cells
        position = [random.randrange(config.nb_cells),
                    random.randrange(config.nb_cells)]
        self.make_body(position)

    def make_body(self, position: list[int]):
        """Initializes the snake's body based
        on the initial position and size.
        """
        pos_x, pos_y = position
        nb_blocks = 0
        down = False
        while nb_blocks < self.size:
            if pos_x + nb_blocks < self.nb_cells:
                self.body.append((pos_x + nb_blocks, pos_y))
                nb_blocks = nb_blocks + 1
            elif down or (self.nb_cells - 1 - pos_y > self.size):
                down = True
                pos_x = self.body[-1][0]
                self.body.append((pos_x, pos_y + 1))
                pos_y = self.body[-1][1]
                nb_blocks = nb_blocks + 1
            else:
                pos_x = self.body[-1][0]
                self.body.append((pos_x, pos_y - 1))
                nb_blocks = nb_blocks + 1
                pos_y = self.body[-1][1]

    def move(self):
        """Moves the snake in the current direction by adding a new head
        in the direction of movement and removing the tail segment.
        """
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction[0], self.direction[1]
        new_head = (head_x + dir_x, head_y + dir_y)
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        """Adds a new segment to the snake's body
        at the position of the current tail.
        """
        tail = self.body[-1]
        self.body.append(tail)

    def shrink(self):
        """Removes the last segment from the snake's body."""
        self.body.pop()

    def change_direction(self, new_direction):
        """Changes the snake's direction if the new direction
        is not directly opposite to the current direction.
        """
        # Prevent the snake from reversing on itself
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def set_direction(self, action: str):
        """Sets the snake's direction based on the given action."""
        match action:
            case "UP":
                self.change_direction((0, -1))
            case "DOWN":
                self.change_direction((0, 1))
            case "LEFT":
                self.change_direction((-1, 0))
            case "RIGHT":
                self.change_direction((1, 0))

    def get_size(self):
        return len(self.body)
