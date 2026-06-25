import random
import pickle
import helpers.const as c
from game.state import State, QTable

EPSILON = 1.0
EPSILON_DECAY = 0.9995
EPSILON_MIN = 0.01
LEARNING_RATE = 0.1
DISCOUNT = 0.9


class QLearningAgent:
    def __init__(self, name, model=None):
        self.set_model_name(model)
        self.epsilon = EPSILON
        self.epsilon_decay = EPSILON_DECAY
        self.epsilon_min = EPSILON_MIN
        self.alpha = LEARNING_RATE
        self.gamma = DISCOUNT
        self.actions = ["UP", "DOWN", "LEFT", "RIGHT"]
        self.name = name

    def set_model_name(self, model_name):
        self.model_name = model_name if model_name else None
        q_table = self.load_model(self.model_name) if self.model_name else None
        self.q_table = q_table if q_table is not None else {}

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
        """Returns the action with the highest Q-value for the given state."""
        q_values = self.get_q_values(state)
        return max(q_values, key=q_values.get)

    def learn(self, state, action, reward, next_state, done):
        """Updates the Q-table based on
        the action taken and the reward received.

        Bellman equation
        Q(s, a) += α * (reward + γ * max(Q(s', a')) - Q(s, a))
        Q(s, a) is the Q-value for a given state-action pair.
        R(s, a) is the immediate reward for taking action a in state s.
        discount_factor (γ): How much future rewards are valued.
        max.α Q(s',a)is the maximum Q-value for the next state s'.
        learning_rate (α): How much new info overrides old info.
        more smooth updates with a lower α, faster learning with a higher α.
        r rewards
        """

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
        with open(f"{c.MODELS_DIR}q_table_{episodes}.pkl", "wb") as file:
            pickle.dump(self.q_table, file)
        # print(self.q_table)

    def load_model(self, path: str = "q_table_10.pkl"):
        if not path.endswith(".pkl"):
            path = f"{c.MODELS_DIR}{path}.pkl"
        else:
            path = f"{c.MODELS_DIR}{path}"
        try:
            with open(path, "rb") as file:
                try:
                    q_table = pickle.load(file)
                    self.q_table_type_check(q_table)
                    return q_table
                except (pickle.UnpicklingError, EOFError, TypeError) as e:
                    print(
                        f"Model file '{path}' is corrupted. {e}")
        except FileNotFoundError:
            print(f"Model file '{path}' not found.")

    def q_table_type_check(self, q_table: QTable):
        """Checks if the loaded Q-table has the correct structure."""
        if not isinstance(q_table, dict):
            raise TypeError("Q-table must be a dictionary.")
        for state, actions in q_table.items():
            if not isinstance(state, State):
                raise TypeError("Q-table keys must be of type State.")
            if not isinstance(actions, dict):
                raise TypeError(
                    "Q-table values must be dictionaries of action values.")
            for action, value in actions.items():
                if action not in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
                    raise TypeError(f"Invalid action '{action}' in Q-table.")
                if not isinstance(value, (int, float)):
                    raise TypeError(
                        f"Q-value for action '{action}' must be a number.")
