import random
import pickle


class QLearningAgent:
    def __init__(self):
        self.q_table = {}
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.alpha = 0.1
        self.gamma = 0.9
        self.actions = ["UP", "DOWN", "LEFT", "RIGHT"]

    def get_q_values(self, state):
        """Returns the Q-values for the given state,
        initializing them to 0 if the state is not in the Q-table.

        It is a mutable variable, so it returns a reference
        to the Q-values dictionary for the state."""
        if state not in self.q_table:
            self.q_table[state] = {action: 0.0 for action in self.actions}
        return self.q_table[state]

    def choose_action(self, state):
        """Chooses an action based on the ε-greedy policy."""
        # exploration_prob (ε): Probability of taking a random action.
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        return self.best_action(state)

    def best_action(self, state):
        q_values = self.get_q_values(state)
        return max(q_values, key=q_values.get)

    def learn(self, state, action, reward, next_state, done):
        """Updates the Q-table based on
        the action taken and the reward received.
        """
        # Bellman equation
        # Q(s, a) += α * (reward + γ * max(Q(s', a')) - Q(s, a))
        # Q(s, a) is the Q-value for a given state-action pair.
        # R(s, a) is the immediate reward for taking action a in state s.
        # discount_factor (γ): How much future rewards are valued.
        # max.α Q(s',a)is the maximum Q-value for the next state s'.
        # learning_rate (α): How much new info overrides old info.
        # more smooth updates with a lower α, faster learning with a higher α.
        # r rewards
        q_values = self.get_q_values(state)
        current_q = q_values[action]

        if done:
            target = reward
        else:
            next_q_values = self.get_q_values(next_state)
            target = reward + self.gamma * max(next_q_values.values())
        q_values[action] = current_q + self.alpha * (target - current_q)

    def decay_epsilon(self):
        """Decays the exploration rate ε after each episode."""
        self.epsilon = max(
            self.epsilon_min,
            self.epsilon * self.epsilon_decay
        )

    def save_model(self, episodes=10):
        with open(f"q_table_{episodes}.pkl", "wb") as file:
            pickle.dump(self.q_table, file)
        print(self.q_table)   

    def load_model(self, path: str = "q_table_10.pkl"):
        with open(path, "rb") as file:
            self.q_table = pickle.load(file)
