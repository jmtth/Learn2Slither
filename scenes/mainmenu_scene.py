import pygame
from scenes.scene import Scene
import render.button_render as button


class MainMenuScene(Scene):

    def __init__(self):
        self.font = pygame.font.SysFont(None, 40)
        self.start_button = button.Button(200, 150, 200, 60, "Start Game", self.start_game,
                                          self.font, (0, 100, 200), (0, 150, 255))

    def handle_event(self, event):
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_RETURN:
        #         self.app.change_scene(GameScene(self.app))
        pass

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((20, 20, 30))
        self.start_button.draw(screen)
        # draw title, buttons, etc.