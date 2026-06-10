import pygame


class AgentController:

    def __init__(self):
        pass

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return False
        if event.key == pygame.K_s:
            return True
        return False
