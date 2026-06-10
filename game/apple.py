# import random
# import const as c
# import pygame


class Apple:
    """Represents an apple in the game.

    Apples can be either green (good) or red (bad).
      """
    def __init__(self, color, position):
        self.color = color
        self.position = position

    def __str__(self):
        return f"Apple(color={self.color}, position={self.position})"
