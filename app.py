import sys
import time
from helpers.parser import Parser
import pygame
import random
import string
from scenes.mainmenu_scene import MainMenuScene
from scenes.agent_scene import AgentScene
from helpers.config import AppConfig
from scenes.scene import Scene
from stats.manage_csv import MyStats
import helpers.const as c
from stats.graph import plot_scores


class App:
    def __init__(self, scene: type[Scene], config: AppConfig):
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

    def change_scene(self, scene: Scene):
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


def generate_id() -> str:
    """Generate a random ID consisting of 15 lowercase letters."""
    return "".join(random.choices(string.ascii_lowercase, k=8))


def load_ai_config(args) -> AppConfig:
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
    app_config.ai.agent_name = generate_id()
    app_config.ai.deep = args.deep
    from game.snake_env import SnakeEnv
    app_config.ai.env = SnakeEnv(app_config)
    if args.deep:
        from ai.DeepQLearning_agent import DeepQAgent
        from ai.Snake_deep_trainer import SnakeDeepTrainer
        app_config.ai.agent = DeepQAgent(app_config.ai.agent_name,
                                         app_config.ai.load_name)
        app_config.ai.trainer = SnakeDeepTrainer(app_config.ai.env,
                                                 app_config.ai.agent)
    else:
        from ai.Qlearning_agent import QLearningAgent
        from ai.Snake_trainer import SnakeTrainer
        app_config.ai.agent = QLearningAgent(app_config.ai.agent_name,
                                             app_config.ai.load_name)
        app_config.ai.trainer = SnakeTrainer(app_config.ai.env,
                                             app_config.ai.agent)
    return app_config


def print_stats(config: AppConfig):
    """ Prints training statistics after AI training is completed. """
    stats = MyStats()
    player = f"{config.ai.agent_name}-{config.ai.sessions}"
    max_length, max_moves, mean_length = stats.get_sessions_stat(player)
    stats_message = f"{c.T_GREEN}\nTraining completed: {c.T_RESET}"
    stats_message += f"Max length: {max_length}, "
    stats_message += f"Max moves: {max_moves} "
    stats_message += f"Mean length: {mean_length} "
    stats_message += f"in {config.ai.sessions} episodes"
    print(stats_message)
    model_path = f"{c.MODELS_DIR}{config.ai.agent_name}"
    model_path += f"_{str(config.ai.sessions)}.pkl"
    print(f"{c.T_GREEN}Model saved as: {c.T_RESET}{model_path}")
    scores, min_score, max_score = stats.get_sessions_scores(player)
    plot_scores(scores, mean_length, min_score, max_score)


def print_duration(start_time: float, end_time: float):
    """Prints the duration of the training in minutes and seconds."""
    # Subtract 5 seconds to account for graph plotting time,
    # which is not part of the actual training duration.
    elapsed_time = end_time - start_time - 5
    minutes = int(elapsed_time // 60)
    seconds = elapsed_time % 60
    message = f"{c.T_GREEN}Training time:{c.T_RESET} {minutes} minutes"
    message += f" and {seconds:.2f} seconds "
    print(message)


def print_info(function, config: AppConfig, pargs):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        if config.ai.learn:
            print(f"\nStarting training for {pargs.sessions} sessions...\n")
            if not pargs.deep:
                print(f"{c.T_GREEN}Q-table:{c.T_RESET}")
        result = function(*args, **kwargs)
        if config.ai.learn:
            print_stats(config)
            end_time = time.perf_counter()
            print_duration(start_time, end_time)
        return result
    return wrapper


def main(argv: list[str] | None = None) -> int:
    args = Parser(argv).args
    if sys.argv[1:] == []:
        warning = f"{c.T_GREEN}Learn2Slither:"
        warning += f" {c.T_RED}need at least one argument{c.T_RESET} {args}"
        print(warning)
        exit(0)

    config = load_ai_config(args)
    if args.human:
        game = App(MainMenuScene, config)
        game.run()
        pygame.quit()
    else:
        if args.visual == "on":
            game = App(AgentScene, config)
            print_info(game.run, config, args)()
            pygame.quit()
        else:
            if config.ai.trainer is None:
                raise RuntimeError("AI trainer is not initialized")
            if config.ai.learn:
                print_info(
                    config.ai.trainer.train, config, args)(args.sessions)
            else:
                print(f"\nStarting evaluation for {args.sessions} episodes.\n")
                config.ai.trainer.play(args.sessions)
    return 0


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{c.T_RED}Learn2Slither Error: {e}{c.T_RESET}")
