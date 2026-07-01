import random
import numpy as np
from collections import deque
from stats.graph import save_DeepQlearning_plot
from tqdm import tqdm


MAX_MEMORY = 100_000
BATCH_SIZE = 256


class SnakeDeepTrainer:
    """A Deep Q-Learning agent for the Snake game.

    This agent uses a neural network to approximate the Q-values
    for each action given the current state of the game.
    It employs an epsilon-greedy strategy for action selection and
    """

    def __init__(self, env, agent):
        self.env = env
        self.agent = agent
        self.memory = deque(maxlen=100_000)

    def get_state(self):
        """Returns the current state of the game as a numpy array.

        The state is represented as a combination of the snake's vision
        in the horizontal and vertical directions,
        as well as the snake's direction.
        state = horizontal + vertical + [dir_x, dir_y]
        W = -1, S = -1, O = 0, R = 1, G = 2
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
        def scan(string: str) -> int:
            """Iterates through the squares in order and returns
            whatever is seen first: 'W', 'G', 'R'.

            The snake's body is treated as a wall
            to minimize the number of states.
            """
            for char in string:
                if is_dangerous(char):
                    return -1  # Wall, Body or Dangerous Red Apple
                if char == 'R':
                    return 1  # Safe Red Apple
                if char == 'G':
                    return 2  # Green Apple
            return -1

        up_state = scan(up_string[::-1])
        down_state = scan(down_string)
        left_state = scan(left_string[::-1])
        right_state = scan(right_string)

        state = [
            float(danger[0]),                    # danger UP
            float(danger[1]),                    # danger DOWN
            float(danger[2]),                    # danger LEFT
            float(danger[3]),                    # danger RIGHT
            float(self.env.snake.direction[0]),  # dir_x
            float(self.env.snake.direction[1]),  # dir_y
            float(up_state),
            float(down_state),
            float(right_state),
            float(left_state),
        ]

        return np.array(state, dtype=np.float32)

    def remember(self, state, action, reward, next_state, done):
        """Stores the experience in the replay memory.
        deque is used to maintain a fixed-size memory buffer.
        it automatically poplefts the oldest experience
        when the buffer is full.
        """
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        """Trains the model using a batch of experiences
        from the replay memory.
        If the memory has more experiences than the batch size,
        a random sample of experiences is used for training.
        Otherwise, all experiences in the memory are used."""
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.agent.learn(states, actions, rewards, next_states, dones)
        # Zip the mini_sample into separate lists for
        # states, actions, rewards, next_states, and dones
        # replaces the for loop below, which was commented out.
        # for state, action, reward, nexrt_state, done in mini_sample:
        #    self.agent.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.agent.learn(state, action, reward, next_state, done)

    def train(self, episodes: int):
        plot_length = []
        plot_mean_length = []
        episode = 0
        total_length = 0
        record = 0

        for _ in tqdm(range(episodes), desc="Training Deep Q-Learning Agent"):
            self.env.reset()
            done = False

            while not done:
                current_state = self.get_state()

                action, action_index = self.agent.choose_action(current_state)

                reward, done = self.env.step(action)
                length = len(self.env.snake.body)

                if not done:
                    next_state = self.get_state()
                else:
                    next_state = current_state
                if self.agent.epsilon < 0.5:
                    self.train_short_memory(current_state,
                                            action_index,
                                            reward,
                                            next_state,
                                            done)
                self.remember(current_state,
                              action_index,
                              reward,
                              next_state,
                              done)
                if done:
                    episode += 1
                    self.train_long_memory()
                    self.agent.decay_epsilon()
                    self.env.save_score(f"{self.agent.name}-{episodes}")

                    if length > record:
                        record = length
                        self.agent.save_model(episodes)

                    plot_length.append(length)
                    total_length += length
                    mean_score = total_length / episode
                    plot_mean_length.append(mean_score)
                    # DeepQlearning_plot(plot_length, plot_mean_length)
        save_DeepQlearning_plot(plot_length, plot_mean_length)

    def learn_step(self, state) -> str:
        """Performs a single learning step for the Deep Q-learning agent.
        This is used for training in the visual mode where the game loop"""
        current_state = state
        action, action_index = self.agent.choose_action(current_state)

        reward, done = self.env.step(action)

        if not done:
            next_state = self.get_state()
        else:
            next_state = state

        self.train_short_memory(current_state,
                                action_index,
                                reward,
                                next_state,
                                done)
        self.remember(current_state, action_index, reward, next_state, done)

        if done:
            self.train_long_memory()

        return action

    def play_step(self, state) -> str:
        """Performs a single play step for the Deep Q-learning agent.
        This is used for playing in the visual mode where the game loop
        is controlled by the AgentScene."""
        action, _ = self.agent.best_action(state)
        self.env.step(action)
        return action

    def play(self, episodes: int):
        """Plays a full game using the Q-learning agent without learning.
        This is used for playing in CLI mode."""
        for _ in range(episodes):
            self.env.reset()
            while not self.env.game_over:
                state = self.get_state()
                action, _ = self.agent.best_action(state)
                self.env.step(action)
                if self.env.game_over:
                    self.env.save_score(f"{self.agent.name}-{episodes}")
