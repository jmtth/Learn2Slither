import pygame
from scenes.scene import Scene
from render.game_render import GameRender
from ai.Qlearning_agent import QLearningAgent
from controllers.agent_controller import AgentController


class AgentScene(Scene):
    """Scene for training and evaluating the AI agent. """
    def __init__(self, app):
        super().__init__(app)
        self.env = app.config.ai.env
        self.env.reset()
        self.renderer = GameRender(app.config)
        self.LearningAgent = app.config.ai.agent
        if app.config.ai.load_name:
            self.LearningAgent.set_model_name(app.config.ai.load_name)
        print(f"Model name: {self.LearningAgent.model_name}")
        self.SnakeTrainer = app.config.ai.trainer
        self.controller = AgentController()
        self.episode = 0
        self.last_move_time = 0
        self.move_delay = app.config.render.ms
        self.start_time = pygame.time.get_ticks()
        self.step_key = app.config.ai.step_by_step
        self.env.print_vision(self.env.fruits)

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
        action = self.SnakeTrainer.learn_step(self.SnakeTrainer.get_state())
        print(f"{action}\n")
        self.env.print_vision(self.env.fruits)
        if self.env.game_over:
            player_name = f"{self.SnakeTrainer.agent.name}"
            player_name += f"-{self.app.config.ai.sessions}"
            self.env.save_score(player_name)
            self.env.reset()
            self.episode += 1
            self.SnakeTrainer.agent.decay_epsilon()
            if self.episode >= self.app.config.ai.sessions:
                if isinstance(self.SnakeTrainer.agent, QLearningAgent):
                    print(self.SnakeTrainer.agent.q_table)
                self.SnakeTrainer.agent.save_model(self.episode)
                self.app.running = False

    def play(self):
        """Performs a simple play step for the Q-learning agent.
        This is used for playing in the visual mode where the game loop
        is controlled by the AgentScene.

        There is a step_by_step mode that allows the user to control
        the pace of the game by pressing the 'S' key to advance
        one step at a time.
        """
        action = "FORWARD"
        if not self.env.game_over and not self.env.paused:
            if self.app.config.ai.step_by_step:
                if self.step_key:
                    action = self.SnakeTrainer.play_step(
                        self.SnakeTrainer.get_state())
                    self.step_key = False
                    print(f"{action}\n")
                    self.env.print_vision(self.env.fruits)
            else:
                now = pygame.time.get_ticks()
                launch_time = now - self.start_time
                if (
                    launch_time > 2000
                    and now - self.last_move_time >= self.move_delay
                ):
                    action = self.SnakeTrainer.play_step(
                        self.SnakeTrainer.get_state())
                    self.last_move_time = now
                    print(f"{action}\n")
                    self.env.print_vision(self.env.fruits)
            if self.env.game_over:
                sessions_name = f"{self.SnakeTrainer.agent.name}"
                sessions_name += f"-{self.app.config.ai.sessions}"
                self.env.save_score(sessions_name)
