# import pygame
from scenes.scene import Scene
from render.game_render import GameRender
from game.snake_env import SnakeEnv
from ai.snake_agent import SnakeAgent
from ai.Qlearning_agent import QLearningAgent
from stats.manage_csv import MyStats


class AgentScene(Scene):
    """Scene for training and evaluating the AI agent. """
    def __init__(self, app):
        super().__init__(app)
        self.env = SnakeEnv(app.config.game)
        self.renderer = GameRender(app.config)
        self.LearningAgent = QLearningAgent()
        self.SnakeAgent = SnakeAgent(self.env, self.LearningAgent)
        self.episode = 0
        # self.trainer.train(app.config.ai.sessions)

    def handle_event(self, event):
        pass

    def update(self):
        if self.app.config.ai.learn:
            self.learn()
        pass

    def draw(self, screen):
        self.renderer.draw(screen, self.env)

    def learn(self):
        self.SnakeAgent.learn_step(self.SnakeAgent.get_state())
        if self.env.game_over:
            # self.env.save_score("Agent")
            self.env.reset()
            self.episode += 1
            self.SnakeAgent.agent.decay_epsilon()
            if self.episode >= self.app.config.ai.sessions:
                self.SnakeAgent.agent.save_model(self.episode)
                max_length = MyStats().get_sessions_stat()
                print(f"Max length: {max_length} in {self.episode} episodes")
                print(f"Debug episodes: {self.app.config.ai.sessions}")
                from scenes.mainmenu_scene import MainMenuScene
                self.app.change_scene(MainMenuScene(self.app))
