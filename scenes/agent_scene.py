import pygame
from scenes.scene import Scene
from render.game_render import GameRender
from game.snake_env import SnakeEnv
from ai.snake_agent import SnakeAgent
from ai.Qlearning_agent import QLearningAgent
from controllers.agent_controller import AgentController


class AgentScene(Scene):
    """Scene for training and evaluating the AI agent. """
    def __init__(self, app):
        super().__init__(app)
        self.env = SnakeEnv(app.config)
        self.renderer = GameRender(app.config)
        self.LearningAgent = QLearningAgent(app.config.ai.agent_name,
                                            app.config.ai.load_name)
        self.SnakeAgent = SnakeAgent(self.env, self.LearningAgent)
        self.controller = AgentController()
        self.episode = 0
        self.last_move_time = 0
        self.move_delay = app.config.render.ms
        self.start_time = pygame.time.get_ticks()
        self.step_key = False

    def handle_event(self, event):
        step = self.controller.handle_event(event)

        if step:
            self.step_key = True
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.step_key = True
            elif event.key == pygame.K_ESCAPE:
                from scenes.ai_settings_scene import AISettings
                self.app.change_scene(AISettings(self.app))

    def update(self):
        if self.app.config.ai.learn:
            self.learn()
        else:
            self.play()
        pass

    def draw(self, screen):
        self.renderer.draw(screen, self.env)

    def learn(self):
        """Performs a simple learning step for the Q-learning agent.
        This is used for training in the visual mode.
        """
        self.SnakeAgent.learn_step(self.SnakeAgent.get_state())
        if self.env.game_over:
            self.env.save_score(
                f"{self.SnakeAgent.agent.name}-{self.app.config.ai.sessions}")
            self.env.reset()
            self.episode += 1
            self.SnakeAgent.agent.decay_epsilon()
            if self.episode >= self.app.config.ai.sessions:
                print(self.SnakeAgent.agent.q_table)
                self.SnakeAgent.agent.save_model(self.episode)
                self.app.running = False

    def play(self):
        """Performs a simple play step for the Q-learning agent.
        This is used for playing in the visual mode where the game loop
        is controlled by the AgentScene.

        There is a step_by_step mode that allows the user to control
        the pace of the game by pressing the 'S' key to advance
        one step at a time.
        """
        if not self.env.game_over and not self.env.paused:
            if self.app.config.ai.step_by_step:
                if self.step_key:
                    self.SnakeAgent.play_step(self.SnakeAgent.get_state())
                    self.step_key = False
            else:
                now = pygame.time.get_ticks()
                launch_time = now - self.start_time
                if (
                    launch_time > 2000
                    and now - self.last_move_time >= self.move_delay
                ):
                    self.SnakeAgent.play_step(self.SnakeAgent.get_state())
                    self.last_move_time = now
            if self.env.game_over:
                sessions_name = f"{self.SnakeAgent.agent.name}"
                sessions_name += f"-{self.app.config.ai.sessions}"
                self.env.save_score(sessions_name)
