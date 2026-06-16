import random
import numpy as np
from collections import deque
from ai.DeepQLearning_model import DeepQModel
from ai.DeepQLearning_agent import DeepQAgent
from stats.graph import DeepQlearning_plot, save_DeepQlearning_plot


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
INPUT_SIZE = 26
HIDDEN_SIZE_1 = 128
HIDDEN_SIZE_2 = 64
OUTPUT_SIZE = 4


class Agent:
    """A Deep Q-Learning agent for the Snake game.

    This agent uses a neural network to approximate the Q-values
    for each action given the current state of the game.
    It employs an epsilon-greedy strategy for action selection and
    """

    def __init__(self, env, agent):
        self.env = env
        self.agent = agent
        self.memory = deque(maxlen=100_000)
        self.model = DeepQModel(INPUT_SIZE,
                                HIDDEN_SIZE_1,
                                HIDDEN_SIZE_2,
                                OUTPUT_SIZE)
        self.trainer = DeepQAgent(self.model)

    def get_state(self):
        """Returns the current state of the game as a numpy array.

        The state is represented as a combination of the snake's vision
        in the horizontal and vertical directions,
        as well as the snake's direction.
        state = horizontal + vertical + [dir_x, dir_y]
        W = -1, S = -0.5, O = 0, H = 0.5, R = 1, G = 2
        """
        head_x, head_y = self.env.snake.body[0]
        vision_grid = self.env.vision(self.env.fruits)
        vertical_vision = "".join(vision_grid[i][head_x + 1]
                                  for i in range(len(vision_grid)))
        horizontal_vision = "".join(vision_grid[head_y + 1][i]
                                    for i in range(len(vision_grid[0])))

        def get_element_value(char: str) -> float:
            if char == 'W':
                return -1
            if char == 'S':
                return -0.5
            if char == 'H':
                return 0.5
            if char == 'R':
                return 1
            if char == 'G':
                return 2
            return 0

        state = [get_element_value(c) for c in horizontal_vision]
        state.extend([get_element_value(c) for c in vertical_vision])
        state.extend([head_x, head_y])

        return np.array(state, dtype=int)

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
        self.trainer.learn(states, actions, rewards, next_states, dones)
        # Zip the mini_sample into separate lists for
        # states, actions, rewards, next_states, and dones
        # replaces the for loop below, which was commented out.
        # for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.learn(state, action, reward, next_state, done)

    def train(self, episodes: int):
        plot_length = []
        plot_mean_length = []
        episode = 0
        total_length = 0
        record = 0

        for episode in range(episodes):
            current_state = self.get_state()

            action, action_index = self.agent.choose_action(current_state)

            reward, done = self.env.play_step(action)
            length = len(self.env.snake.body)
            next_state = self.get_state()

            self.train_short_memory(current_state, action_index, reward, next_state, done)
            self.remember(current_state, action_index, reward, next_state, done)

            if done:
                self.env.reset()
                episode += 1
                self.train_long_memory()

                if length > record:
                    record = length
                    self.model.save()

                print('Game', episode, 'Length', length, 'Record:', record)

                plot_length.append(length)
                total_length += length
                mean_score = total_length / episode
                plot_mean_length.append(mean_score)
                DeepQlearning_plot(plot_length, plot_mean_length)
        save_DeepQlearning_plot(plot_length, plot_mean_length)
