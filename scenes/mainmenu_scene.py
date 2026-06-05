import pygame
from scenes.scene import Scene
from scenes.game_scene import GameScene
from scenes.game_settings import GameSettings
import render.button_render as button
import const as c


class MainMenuScene(Scene):

    def __init__(self, app):
        self.app = app
        self.font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 18)
        self.font_title = pygame.font.Font(
            "assets/PressStart2P-Regular.ttf", 26)

        self.start_button = button.Button(200, 150, 200, 60,
                                          "Start Game",
                                          self.start_game,
                                          self.font,
                                          c.BLUE_BUTTON,
                                          c.BLUE_HOVER,
                                          c.BLUE_CLICK)
        self.settings_button = button.Button(200, 250, 200, 60,
                                             "Settings",
                                             self.open_settings,
                                             self.font,
                                             c.BLUE_BUTTON,
                                             c.BLUE_HOVER,
                                             c.BLUE_CLICK)
        self.quit_button = button.Button(200, 350, 200, 60,
                                         "Quit",
                                         self.quit_game,
                                         self.font,
                                         c.RED_BUTTON,
                                         c.RED_HOVER,
                                         c.RED_CLICK)

    def start_game(self):
        self.app.change_scene(GameScene(self.app))
        pass

    def open_settings(self):
        self.app.change_scene(GameSettings(self.app))
        pass

    def quit_game(self):
        self.app.running = False

    def handle_event(self, event):
        self.start_button.handle_event(event)
        self.settings_button.handle_event(event)
        self.quit_button.handle_event(event)

    def update(self):
        pass

    def draw(self, screen):
        pygame.display.set_caption('Learn2Slither Snake: Main Menu')
        screen.fill(c.BLACK)
        title = self.font_title.render("MAIN MENU", True, c.GREEN)
        screen.blit(title, title.get_rect(
            center=(self.app.config.render.screen_width // 2, 80)))
        self.start_button.draw(screen)
        self.settings_button.draw(screen)
        self.quit_button.draw(screen)

        # draw title, buttons, etc.
