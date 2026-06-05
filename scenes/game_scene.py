import const as c
import pygame
from scenes.scene import Scene
from render.game_render import GameRender
from game.snake_env import SnakeEnv
from controllers.human_controller import HumanController


class GameScene(Scene):
    """Main game scene where the snake game is played. """
    def __init__(self, app):
        super().__init__(app)
        self.gameover = False
        self.pending_action = None
        self.score = 0
        self.pause = True
        self.env = SnakeEnv(app.config.game)
        self.renderer = GameRender(app.config)
        self.last_move_time = 0
        self.move_delay = app.config.render.ms

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.pending_action = "UP"
            elif event.key == pygame.K_DOWN:
                self.pending_action = "DOWN"
            elif event.key == pygame.K_LEFT:
                self.pending_action = "LEFT"
            elif event.key == pygame.K_RIGHT:
                self.pending_action = "RIGHT"
            elif event.key == pygame.K_ESCAPE: 
                from scenes.mainmenu_scene import MainMenuScene
                self.app.change_scene(MainMenuScene(self.app))
                self.gameover = False
                self.score = 0
            elif event.key == pygame.K_p:
                self.pause = not self.pause

    def update(self):
        if not self.gameover or not self.pause:
            now = pygame.time.get_ticks()

            if now - self.last_move_time >= self.move_delay:
                self.env.step(self.pending_action)
                self.pending_action = None
                self.last_move_time = now
            self.score = self.env.score
            self.gameover = self.env.game_over

    def draw(self, screen):
        self.renderer.draw(screen, self.env)
