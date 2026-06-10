from parser import Parser
import pygame
from scenes.mainmenu_scene import MainMenuScene
from scenes.agent_scene import AgentScene
from config import AppConfig
from stats.manage_csv import MyStats
import const as c


class App:
    def __init__(self, scene, config):
        self.config = config
        pygame.init()
        pygame.display.set_caption('Learn2Slither Snake')
        self.screen = pygame.display.set_mode(
            (self.config.render.screen_width,
             self.config.render.screen_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.pause = True
        self.scene = scene(self)
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
    app_config.ai.load_name = args.load if args.load else None
    app_config.ai.save_name = args.save
    app_config.ai.learn = not args.dontlearn
    app_config.ai.step_by_step = args.step_by_step
    return app_config


def print_stats(config, player="Agent"):
    """ Prints training statistics after AI training is completed. """
    stats = MyStats()
    player = f"{player}-{config.ai.sessions}"
    max_length, max_moves = stats.get_sessions_stat(player)
    stats_message = f"{c.T_GREEN}\nTraining completed: {c.T_RESET}"
    stats_message += f"Max length: {max_length}, "
    stats_message += f"Max moves: {max_moves} "
    stats_message += f"in {config.ai.sessions} episodes"
    print(stats_message)
    model_path = f"{config.ai.models_path}{config.ai.save_name}"
    model_path += f"_{str(config.ai.sessions)}.pkl"
    print(f"{c.T_GREEN}Model saved as: {c.T_RESET}{model_path}")


def main(argv: list[str] | None = None) -> int:
    args = Parser(argv).args

    if args.human:
        game = App(MainMenuScene, AppConfig())
        game.run()
        pygame.quit()
    else:
        config = load_ai_config(args)
        if args.visual == "on":
            game = App(AgentScene, config)
            print(f"\nStarting training for {args.sessions} sessions...\n")
            print(f"{c.T_GREEN}Q-table:{c.T_RESET}")
            game.run()
            print_stats(config, player="AgentV")
            pygame.quit()
        else:
            from ai.Qlearning_agent import QLearningAgent
            from game.snake_env import SnakeEnv
            from ai.snake_agent import SnakeAgent
            env = SnakeEnv(config.game)
            agent = QLearningAgent(config.ai.load_name)
            trainer = SnakeAgent(env, agent)
            print(f"\nStarting training for {args.sessions} sessions...\n")
            print(f"{c.T_GREEN}Q-table:{c.T_RESET}")
            trainer.train(args.sessions)
            print_stats(config, player="Agent")
    return 0


if __name__ == "__main__":
    main()
