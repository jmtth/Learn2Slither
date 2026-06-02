import random
import const as c
import pygame
import apple

class Snake:
    def __init__(self, initial_position, speed = 15, size=3):
        self.position = initial_position  # List of (x, y) tuples representing the snake's body
        self.direction = (-1, 0)  # Initial direction: moving right
        self.speed = speed
        self.size = size
        self.rect = pygame.Rect(initial_position[0], initial_position[1], c.CELL_SIZE, c.CELL_SIZE)
        self.body = [(initial_position[0] + c.CELL_SIZE*i, initial_position[1]) for i in range(size)]  # Initialize the body with the initial position
        print(f"Initial snake body: {self.body}")  # Debug print to check initial body positions

    def move(self, fruits):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction[0] * c.CELL_SIZE, self.direction[1] * c.CELL_SIZE
        new_head = (head_x + dir_x, head_y + dir_y)
        self.rect.topleft = new_head  # Update the rect position to the new head position
        self.body.insert(0, new_head)  # Add new head to the front of the body
        growth = False
        score = 0
        # Check for collision with fruits
        for fruit in fruits:
            if self.rect.colliderect(pygame.Rect(fruit.position[0], fruit.position[1], c.CELL_SIZE, c.CELL_SIZE)):
                print(f"Snake ate a fruit at {fruit.position}!")
                if fruit.color == c.RED:
                    print("Red fruit eaten! Snake's length decrease by 1.")
                    self.body.pop()
                    score -= 10  # Decrease score for eating red fruit
                else:      # Remove the tail segment to decrease length
                    growth = True
                    score += 10  # Increase score for eating green fruit
                fruit.respawn(self.body)  # Respawn the fruit at a new position
                break  # Exit the loop after eating a fruit
        if not growth:
            self.body.pop()  # Remove the tail
        return score

    def grow(self):
        tail = self.body[-1]
        self.body.append(tail)  # Add a new segment at the tail position

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, c.GREEN, (segment[0], segment[1], c.CELL_SIZE, c.CELL_SIZE))

    def change_direction(self, new_direction):
        # Prevent the snake from reversing on itself
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction
    
    def get_size(self):
        return len(self.body)
