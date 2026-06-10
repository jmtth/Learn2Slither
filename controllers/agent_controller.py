import pygame


class AgentController:

    def __init__(self):
        pass

    def handle_event(self, event):
        """Handles user input events to control the agent's behavior.
        Specifically, it listens for the 'S' key to trigger a step
        in the game loop when in step-by-step mode.
        """
        if event.type != pygame.KEYDOWN:
            return False
        if event.key == pygame.K_s:
            return True
        return False
