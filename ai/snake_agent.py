from game.state import State, Object
from game.snake_env import SnakeEnv
from ai.Qlearning_agent import QLearningAgent
from game.state import State


class SnakeAgent:
    def __init__(self, env: SnakeEnv, agent: QLearningAgent):
        self.env = env
        self.agent = agent

    def get_state(self):
        """Encodes the current state of the game into a format
        suitable for the Q-learning agent.
        """
        head_x, head_y = self.env.snake.body[0]
        vision_grid = self.env.vision(self.env.fruits)
        up_string = "".join(vision_grid[i][head_x + 1]
                            for i in range(head_y + 1))
        down_string = "".join(vision_grid[i][head_x + 1]
                              for i in range(head_y + 2, len(vision_grid)))
        left_string = "".join(vision_grid[head_y + 1][i]
                              for i in range(head_x + 1))
        right_string = "".join(vision_grid[head_y + 1][i]
                               for i in range(head_x + 2, len(vision_grid[0])))

        def is_dangerous(char: str) -> bool:
            """Determines if a character in the vision grid
            represents a danger to the snake."""
            return (
                char == 'W' or
                char == 'S' or
                (char == 'R' and len(self.env.snake.body) <= 2)
            )

        # Immediate Danger in each direction
        danger = (
            is_dangerous(up_string[-1]),
            is_dangerous(down_string[0]),
            is_dangerous(left_string[-1]),
            is_dangerous(right_string[0]),
        )

        # First object seen on the path
        def scan(string: str) -> Object:
            """Iterates through the squares in order and returns
            whatever is seen first: 'W', 'G', 'R'.

            The snake's body is treated as a wall
            to minimize the number of states.
            """
            for char in string:
                if is_dangerous(char):
                    return 'W'  # Wall, Body or Dangerous Red Apple
                if char == 'G' or char == 'R':
                    return char
            return 'W'

        up_state = scan(up_string[::-1])
        down_state = scan(down_string)
        left_state = scan(left_string[::-1])
        right_state = scan(right_string)

        return State(
            danger=danger,
            direction=self.env.snake.direction,
            up=up_state,
            down=down_state,
            right=right_state,
            left=left_state
        )

    def train(self, episodes: int):
        """Trains the Q-learning agent for a specified number of episodes."""
        for _ in range(episodes):
            self.env.reset()
            state = self.get_state()
            done = False

            while not done:
                action = self.agent.choose_action(state)
                reward, done = self.env.step(action)
                if not done:
                    next_state = self.get_state()
                else:
                    next_state = state
                    self.env.save_score(f"{self.agent.name}-{episodes}")
                self.agent.learn(
                    state,
                    action,
                    reward,
                    next_state,
                    done
                )
                state = next_state
            self.agent.decay_epsilon()

        print(self.agent.q_table)
        self.agent.save_model(episodes)

    def learn_step(self, state: State):
        """Performs a single learning step for the Q-learning agent.
        This is used for training in the visual mode where the game loop
        is controlled by the AgentScene."""
        action = self.agent.choose_action(state)
        reward, done = self.env.step(action)
        if not done:
            next_state = self.get_state()
        else:
            next_state = state
        self.agent.learn(
            state,
            action,
            reward,
            next_state,
            done
        )

    def play_step(self, state: State):
        """Performs a single step for the Q-learning agent without learning.
        This is used for playing in the visual mode where the game loop
        is controlled by the AgentScene."""
        action = self.agent.best_action(state)
        self.env.step(action)

    def play(self, episodes: int):
        """Plays a full game using the Q-learning agent without learning.
        This is used for playing in the visual mode where the game loop
        is controlled by the AgentScene."""
        for _ in range(episodes):
            self.env.reset()
            while not self.env.game_over:
                state = self.get_state()
                action = self.agent.best_action(state)
                self.env.step(action)
                if self.env.game_over:
                    self.env.save_score(f"{self.agent.name}-{episodes}")
