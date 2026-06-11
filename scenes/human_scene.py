import pygame
from scenes.scene import Scene
from render.game_render import GameRender
from game.snake_env import SnakeEnv
from controllers.human_controller import HumanController


class HumanScene(Scene):
    """Main game scene where the snake game is played. """
    def __init__(self, app):
        super().__init__(app)
        self.pending_action = None
        self.env = SnakeEnv(app.config)
        self.gameover = self.env.game_over
        self.pause = self.env.paused
        self.renderer = GameRender(app.config)
        self.controller = HumanController()
        self.last_move_time = 0
        self.move_delay = app.config.render.ms
        self.start_time = pygame.time.get_ticks()
        self.env.print_vision(self.env.fruits)

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
                    self.do_step()
            else:
                now = pygame.time.get_ticks()
                launch_time = now - self.start_time
                if (
                    launch_time > 2000
                    and now - self.last_move_time >= self.move_delay
                ):
                    self.do_step()
                    self.last_move_time = now
            self.gameover = self.env.game_over
            if self.gameover:
                self.env.save_score("Human")

    def do_step(self):

        self.env.step(self.pending_action)
        if self.pending_action:
            print(f"{self.pending_action}\n")
        else:
            print("FORWARD\n")
        self.env.print_vision(self.env.fruits)
        self.pending_action = None

    def draw(self, screen):
        self.renderer.draw(screen, self.env)
