# import pygame
from scenes.scene import Scene
from render.game_render import GameRender
from game.snake_env import SnakeEnv
from ai.snake_agent import SnakeAgent
from ai.Qlearning_agent import QLearningAgent


class AgentScene(Scene):
    """Scene for training and evaluating the AI agent. """
    def __init__(self, app):
        super().__init__(app)
        self.env = SnakeEnv(app.config.game)
        self.renderer = GameRender(app.config)
        self.LearningAgent = QLearningAgent()
        self.SnakeAgent = SnakeAgent(self.env, self.LearningAgent)
        # self.trainer.train(app.config.ai.sessions)

    def handle_event(self, event):
        pass

    def update(self):
        self.SnakeAgent.learn_step(self.SnakeAgent.get_state())   # Train for one episode at a time to allow rendering
        pass

    def draw(self, screen):
        self.renderer.draw(screen, self.env)
