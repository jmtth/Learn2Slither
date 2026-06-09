import pygame
# from scenes.game_scene import GameScene
from scenes.mainmenu_scene import MainMenuScene
from config import AppConfig
import argparse


class App:
    def __init__(self):
        self.config = AppConfig()
        pygame.init()
        pygame.display.set_caption('Learn2Slither Snake')
        self.screen = pygame.display.set_mode(
            (self.config.render.screen_width,
             self.config.render.screen_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.pause = True
        self.scene = MainMenuScene(self)
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sessions",
        dest="sessions",
        type=int,
        default=10,
        help="Number of sessions to learn.",
    )
    parser.add_argument(
        "--learning",
        dest="learning",
        type=bool,
        default=False,
        help="Learning mode, True or False.",
    )
    parser.add_argument(
        "--graphic",
        dest="graphic",
        default=True,
        help="Path where the generated responses should be written.",
    )
    args = parser.parse_args(argv)

    # run_cli(args.functions_definition, args.input_path, args.output_path)

    if not args.learning:
        game = App()
        game.run()
        pygame.quit()
    else:
        from ai.Qlearning_agent import QLearningAgent
        from game.snake_env import SnakeEnv
        from ai.Snake_agent import SnakeAgent
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
