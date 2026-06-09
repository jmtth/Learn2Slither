import pygame
from scenes.scene import Scene
from render.game_render import GameRender
from game.snake_env import SnakeEnv
from controllers.human_controller import HumanController
import csv
import datetime
import os


class HumanScene(Scene):
    """Main game scene where the snake game is played. """
    def __init__(self, app):
        super().__init__(app)
        self.pending_action = None
        self.env = SnakeEnv(app.config.game)
        self.gameover = self.env.game_over
        self.pause = self.env.paused
        self.renderer = GameRender(app.config)
        self.controller = HumanController()
        self.last_move_time = 0
        self.move_delay = app.config.render.ms
        self.start_time = pygame.time.get_ticks()

    def handle_event(self, event):
        action = self.controller.handle_event(event)

        if action is not None:
            self.pending_action = action

        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from scenes.mainmenu_scene import MainMenuScene
                self.app.change_scene(MainMenuScene(self.app))
            elif event.key == pygame.K_p:
                self.pause = not self.pause
                self.env.paused = self.pause

    def update(self):
        if not self.gameover and not self.pause:
            if self.app.config.render.step_by_step:
                if self.pending_action:
                    self.env.vision(self.env.fruits)
                    self.env.step(self.pending_action)
                    self.pending_action = None
            else:
                now = pygame.time.get_ticks()
                launch_time = now - self.start_time
                if (
                    launch_time > 2000
                    and now - self.last_move_time >= self.move_delay
                ):
                    self.env.vision(self.env.fruits)
                    self.env.step(self.pending_action)
                    print("FORWARD\n")
                    self.pending_action = None
                    self.last_move_time = now
            self.gameover = self.env.game_over
            if self.gameover:
                self.save_score()

    def draw(self, screen):
        self.renderer.draw(screen, self.env)

    def save_score(self):
        if not os.path.exists('scores.csv'):
            with open('scores.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Player",
                                 "Date",
                                 "Moves",
                                 "Length",
                                 "Green Apples",
                                 "Red Apples"])
        with open('scores.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow(["Human",
                             date,
                             self.env.move_count,
                             self.env.snake.get_size(),
                             self.env.green_apples_eaten,
                             self.env.red_apples_eaten])
