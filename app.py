from parser import Parser
import pygame
from scenes.mainmenu_scene import MainMenuScene
from scenes.agent_scene import AgentScene
from config import AppConfig


class App:
    def __init__(self, scene=None):
        self.config = AppConfig()
        pygame.init()
        pygame.display.set_caption('Learn2Slither Snake')
        self.screen = pygame.display.set_mode(
            (self.config.render.screen_width,
             self.config.render.screen_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.pause = True
        self.scene = scene(self) if scene else MainMenuScene(self)
        self.gameover = False
        self.score = 0
        self.pause = True

    def change_scene(self, scene):
        self.scene = scene

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.scene.handle_event(event)

            self.scene.update()
            self.scene.draw(self.screen)
            self.clock.tick(self.config.render.fps)
            pygame.display.flip()


def load_ai_config(args):
    """ Loads AI configuration from command-line
    arguments into the AppConfig.
    """
    app_config = AppConfig()
    app_config.ai.sessions = args.sessions
    app_config.ai.visual = args.visual
    app_config.ai.load_name = args.load
    app_config.ai.save_name = args.save
    app_config.ai.learn = not args.dontlearn
    app_config.ai.step_by_step = args.step_by_step
    return app_config


def main(argv: list[str] | None = None) -> int:
    args = Parser(argv).args

    if args.human:
        game = App(MainMenuScene)
        game.run()
        pygame.quit()
    else:
        load_ai_config(args)
        if args.visual == "on":
            game = App(AgentScene)
            game.run()
            pygame.quit()
        else:
            from ai.Qlearning_agent import QLearningAgent
            from game.snake_env import SnakeEnv
            from ai.snake_agent import SnakeAgent
            config = AppConfig()
            env = SnakeEnv(config.game)
            agent = QLearningAgent()
            trainer = SnakeAgent(env, agent)
            trainer.train(args.sessions)
    return 0


if __name__ == "__main__":
    # game = App()
    # game.run()
    # pygame.quit()
    main()
