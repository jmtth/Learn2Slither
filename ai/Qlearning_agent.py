import random


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
        # mutable variable return a ref
        if state not in self.q_table:
            self.q_table[state] = {action: 0.0 for action in self.actions}
        return self.q_table[state]

    def choose_action(self, state):
        # exploration_prob (ε): Probability of taking a random action.
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        q_values = self.get_q_values(state)
        return max(q_values, key=q_values.get)

    def learn(self, state, action, reward, next_state, done):
        # Bellman equatiom
        # Q[s, a] := Q[s, a] + α[r + γ maxa' Q(s', a') - Q(s, a)]
        # Q(s, a) is the Q-value for a given state-action pair.
        # R(s, a) is the immediate reward for taking action a in state s.
        # discount_factor (γ): How much future rewards are valued.
        # max.α Q(s',a)is the maximum Q-value for the next state s'.
        # learning_rate (α): How much new info overrides old info.
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
        return max(
            self.epsilon_min,
            self.epsilon * self.epsilon_decay
        )
