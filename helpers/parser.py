
import argparse
import pickle
from game.state import State, QTable
import helpers.const as c


class Parser:
    """Parser for command-line arguments to configure
    the snake agent's training and gameplay settings.
    """
    def __init__(self, argv: list[str] | None = None):
        self.argv = argv
        info = "A snake that learns how to behave in an environment through"
        info += " trial and error, using the Q-learning algorithm."
        parser = argparse.ArgumentParser(description=info)
        self.parser = parser
        self.add_arguments(self.parser)
        args = self.parser.parse_args(self.argv)
        self.args = args
        self.check_arguments()

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            "-sessions",
            type=int,
            default=0,
            help="Number of training sessions for the snake agent.",
        )
        parser.add_argument(
            "-save", "-s",
            type=str,
            default="q_table",
            help="Name of model file to be saved.",
        )
        parser.add_argument(
            "-visual",
            type=str,
            choices=['on', 'off'],
            default="on",
            help="Enable visual mode to see the snake learning in real-time.",
        )
        parser.add_argument(
            "-load",
            type=str,
            help="Name of the model to be loaded.",
        )
        parser.add_argument(
            "-dontlearn",
            action="store_true",
            help="Disable learning mode for the snake agent.",
        )
        parser.add_argument(
            "-step_by_step",
            action="store_true",
            help="Enable step-by-step learning mode."
        )
        parser.add_argument(
            "-human",
            action="store_true",
            help="Play the game as a human player."
        )
        parser.add_argument(
            "-deep",
            action="store_true",
            help="Enable deep learning mode for the snake agent."
        )

    def check_arguments(self):
        """Checks the validity of the parsed arguments."""
        if self.args.human:
            self.args.dontlearn = True
            return  # No further checks needed for human play
        if self.args.sessions < 0 or self.args.sessions > 100000:
            self.parser.error(
                "Number of sessions must be between 0 and 10,000.")
        if not self.args.dontlearn and self.args.sessions == 0:
            self.parser.error(
                "sessions must be greater than 0 when learning is enabled.")
        if self.args.load:
            file_name = f"{c.MODELS_DIR}{self.args.load}.pkl"
            try:
                with open(file_name, "rb") as file:
                    try:
                        q_table = pickle.load(file)
                        self.q_table_type_check(q_table)
                    except (pickle.UnpicklingError, EOFError):
                        self.parser.error(
                            f"Model file '{file_name}' is corrupted.")
            except FileNotFoundError:
                self.parser.error(f"Model file '{file_name}' not found.")
        if self.args.step_by_step and not self.args.visual == "on":
            self.parser.error(
                "Step-by-step mode requires visual mode to be enabled.")
        if self.args.dontlearn and not self.args.load:
            self.parser.error(
                "Cannot disable learning without loading a model.")

    def q_table_type_check(self, q_table: QTable):
        """Checks if the loaded Q-table has the correct structure."""
        if not isinstance(q_table, dict):
            self.parser.error(
                "Q-table must be a dictionary.")
        for state, actions in q_table.items():
            if not isinstance(state, State):
                self.parser.error(
                    "Q-table keys must be of type State.")
            if not isinstance(actions, dict):
                self.parser.error(
                    "Q-table values must be dictionaries of action values.")
            for action, value in actions.items():
                if action not in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
                    self.parser.error(
                        f"Invalid action '{action}' in Q-table.")
                if not isinstance(value, (int, float)):
                    self.parser.error(
                        f"Q-value for action '{action}' must be a number.")
