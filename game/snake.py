import const as c
import random


class Snake:
    """Represents the snake in the game."""
    def __init__(self, config):
        self.body = []
        self.direction = (-1, 0)  # Initial direction: moving right
        self.size = config.initial_size
        self.nb_cells = config.nb_cells
        position = [random.randrange(config.nb_cells),
                    random.randrange(config.nb_cells)]
        self.make_body(position)
        # Debug print to check initial body positions
        print(f"Initial snake body: {self.body}")

    def make_body(self, position):
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
        self.body.insert(0, new_head)  # Add new head to the front of the body
        self.body.pop()  # Remove the tail

    def vision(self, fruits):
        pass
        # head_x, head_y = self.body[0]

        # body_positions = set(self.body[1:])
        # fruit_map = {
        #     tuple(fruit.position): fruit
        #     for fruit in fruits
        # }

        # vision_data = [
        #     [" " for _ in range(c.NB_CELLS + 2)]
        #     for _ in range(c.NB_CELLS + 2)
        # ]

        # for i in range(c.NB_CELLS+2):
        #     for j in range(c.NB_CELLS+2):
        #         if (
        #             i == 0
        #             or j == 0
        #             or i == c.NB_CELLS + 1
        #             or j == c.NB_CELLS + 1
        #         ):
        #             if (i==0 and j >0) or (i==c.NB_CELLS+1 and j > 0):
        #                 cell_x = (j - 1) * c.CELL_SIZE
        #                 if cell_x == head_x:
        #                     vision_data[i][j] = "W"
        #             if (j == 0 and i > 0) or (j==c.NB_CELLS+1 and i > 0):
        #                 cell_y = (i - 1) * c.CELL_SIZE
        #                 if cell_y == head_y:
        #                     vision_data[i][j] = "W"
        #             continue

        #         cell_x = (j - 1) * c.CELL_SIZE
        #         cell_y = (i - 1) * c.CELL_SIZE

        #         if cell_x == head_x or cell_y == head_y:
        #             vision_data[i][j] = "O"

        #         if (cell_x, cell_y) == (head_x, head_y):
        #             vision_data[i][j] = "H"

        #         if (cell_x, cell_y) in body_positions and (cell_x == head_x or cell_y == head_y):
        #             vision_data[i][j] = "S"

        #         if fruit := fruit_map.get((cell_x, cell_y)):
        #             if cell_x == head_x or cell_y == head_y:
        #                 vision_data[i][j] = (
        #                     "G" if fruit.color == c.GREEN else "R"
        #                 )

        # for row in vision_data:
        #     print("".join(row))
        # print("\n")
        # return vision_data

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

    def set_direction(self, action):
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
