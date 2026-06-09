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
        self.episode = 0
        # self.trainer.train(app.config.ai.sessions)

    def handle_event(self, event):
        pass

    def update(self):
        self.SnakeAgent.learn_step(self.SnakeAgent.get_state())
        if self.env.game_over:
            self.env.save_score("Agent")
            self.env.reset()
            self.episode += 1
            if self.episode >= self.app.config.ai.sessions:
                self.SnakeAgent.agent.save_model(self.episode)
                from scenes.mainmenu_scene import MainMenuScene
                self.app.change_scene(MainMenuScene(self.app))
        pass

    def draw(self, screen):
        self.renderer.draw(screen, self.env)
