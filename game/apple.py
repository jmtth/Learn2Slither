# import random
# import const as c
# import pygame


class Apple:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        # Debug print to check initial position
        print(f"Initial apple position: {self.position}")

    def __str__(self):
        return f"Apple(color={self.color}, position={self.position})"

    # def draw(self, screen):
    #     pygame.draw.rect(screen, self.color, (self.position[0], self.position[1], c.CELL_SIZE, c.CELL_SIZE))

    # def respawn(self, snake_body, fruits):
    #     while True:
    #         new_position = [random.randrange(1, c.NB_CELLS) * c.CELL_SIZE,
    #                         random.randrange(1, c.NB_CELLS) * c.CELL_SIZE]
    #         if new_position not in snake_body and new_position not in [fruit.position for fruit in fruits]:
    #             self.position = new_position
    #             break