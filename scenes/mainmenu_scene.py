import pygame
from scenes.scene import Scene
from scenes.human_scene import HumanScene
from scenes.game_settings_scene import GameSettings
from scenes.stats_scene import StatsScene
from scenes.agent_scene import AgentScene
import render.button_render as button
import const as c


class MainMenuScene(Scene):

    def __init__(self, app):
        self.app = app
        self.font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 18)
        self.font_title = pygame.font.Font(
            "assets/PressStart2P-Regular.ttf", 26)

        pos_x = (self.app.config.render.screen_width - 200) // 2
        pos_y = 250

        self.start_button = button.Button(pos_x-150, pos_y, 200, 60,
                                          "Start Game",
                                          self.start_game,
                                          self.font,
                                          c.BLUE_BUTTON,
                                          c.BLUE_HOVER,
                                          c.BLUE_CLICK)
        self.ai_button = button.Button(pos_x+150, pos_y, 200, 60,
                                       "AI Game",
                                       self.start_ai_game,
                                       self.font,
                                       c.BLUE_BUTTON,
                                       c.BLUE_HOVER,
                                       c.BLUE_CLICK)
        self.settings_button = button.Button(pos_x+150, pos_y + 150, 200, 60,
                                             "Settings",
                                             self.open_settings,
                                             self.font,
                                             c.BLUE_BUTTON,
                                             c.BLUE_HOVER,
                                             c.BLUE_CLICK)
        self.stats_button = button.Button(pos_x-150, pos_y + 150, 200, 60,
                                          "Stats",
                                          self.open_stats,
                                          self.font,
                                          c.BLUE_BUTTON,
                                          c.BLUE_HOVER,
                                          c.BLUE_CLICK)
        self.quit_button = button.Button(pos_x, pos_y + 300, 200, 60,
                                         "Quit",
                                         self.quit_game,
                                         self.font,
                                         c.RED_BUTTON,
                                         c.RED_HOVER,
                                         c.RED_CLICK)

        self.buttons = [self.start_button,
                        self.ai_button,
                        self.settings_button,
                        self.stats_button,
                        self.quit_button]
        self.buttons_index = 0
        self.start_button.hovered = True

    def start_game(self):
        self.app.change_scene(HumanScene(self.app))

    def start_ai_game(self):
        self.app.change_scene(AgentScene(self.app))

    def open_settings(self):
        self.app.change_scene(GameSettings(self.app))

    def open_stats(self):
        self.app.change_scene(StatsScene(self.app))

    def quit_game(self):
        self.app.running = False

    def handle_event(self, event):
        for but in self.buttons:
            but.handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.buttons[self.buttons_index].hovered = False
                self.buttons_index = (
                    (self.buttons_index - 1)
                    % len(self.buttons)
                    )
                self.buttons[self.buttons_index].hovered = True
            elif event.key == pygame.K_DOWN:
                self.buttons[self.buttons_index].hovered = False
                self.buttons_index = (
                    (self.buttons_index + 1)
                    % len(self.buttons)
                    )
                self.buttons[self.buttons_index].hovered = True
            # elif event.key == pygame.K_RETURN:
            #     if self.start_button.hovered:
            #         self.start_game()
            #     elif self.settings_button.hovered:
            #         self.open_settings()
            #     elif self.quit_button.hovered:
            #         self.quit_game()
            elif event.key == pygame.K_ESCAPE:
                self.quit_game()

    def update(self):
        pass

    def draw(self, screen):
        pygame.display.set_caption('Learn2Slither Snake: Main Menu')
        screen.fill(c.BLACK)
        title = self.font_title.render("MAIN MENU", True, c.GREEN)
        screen.blit(title, title.get_rect(
            center=(self.app.config.render.screen_width // 2, 100)))
        self.start_button.draw(screen)
        self.ai_button.draw(screen)
        self.settings_button.draw(screen)
        self.stats_button.draw(screen)
        self.quit_button.draw(screen)
