import torch
import torch.optim as optim
import torch.nn as nn
import random
import numpy as np
from ai.DeepQLearning_model import DeepQModel


EPSILON = 1.0
EPSILON_DECAY = 0.9995
EPSILON_MIN = 0.01
LEARNING_RATE = 0.001
DISCOUNT = 0.9
INPUT_SIZE = 10
HIDDEN_SIZE_1 = 64
HIDDEN_SIZE_2 = 32
OUTPUT_SIZE = 4


DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class DeepQAgent:
    def __init__(self, name, load_name=None, save_name=None):
        self.name = name
        self.save_name = save_name
        self.set_model_name(load_name)
        self.epsilon = EPSILON
        self.gamma = DISCOUNT
        self.epsilon_decay = EPSILON_DECAY
        self.epsilon_min = EPSILON_MIN
        self.actions = ["UP", "DOWN", "LEFT", "RIGHT"]

    def set_model_name(self, model_name):
        self.model_name = model_name if model_name else None
        self.model = DeepQModel(INPUT_SIZE,
                                HIDDEN_SIZE_1,
                                HIDDEN_SIZE_2,
                                OUTPUT_SIZE,
                                self.model_name).to(DEVICE)
        self.optimizer = optim.Adam(self.model.parameters(), lr=LEARNING_RATE)
        self.criterion = nn.MSELoss()

    def learn(self, state, action, reward, next_state, done):
        # 1: Convert data to tensor
        state = torch.as_tensor(np.array(state),
                                dtype=torch.float32, device=DEVICE)
        next_state = torch.as_tensor(np.array(next_state),
                                     dtype=torch.float32, device=DEVICE)
        action = torch.as_tensor(action, dtype=torch.long, device=DEVICE)
        reward = torch.as_tensor(reward, dtype=torch.float32, device=DEVICE)
        done = torch.as_tensor(done, dtype=torch.bool, device=DEVICE)

        # this case for only on value
        if len(state.shape) == 1:
            state = state.unsqueeze(0)
            next_state = next_state.unsqueeze(0)
            action = action.unsqueeze(0)
            reward = reward.unsqueeze(0)
            done = done.unsqueeze(0)

        # 2: predicted Q values with current state
        pred = self.model(state)

        # 3: Compute the Q value with the Bellman's formula
        target = pred.detach().clone()

        # Compute the Q value with the Bellman's formula
        # Use torch.no_grad() to prevent gradient computation for next_q
        with torch.no_grad():
            next_q = self.model(next_state).max(dim=1)[0]
            # we compute only not done sessions, because if done, the next_q
            # is reward only, no future reward is expected
            q_new = reward + self.gamma * next_q * (~done)
        # Update the target Q-values for the chosen actions
        target[torch.arange(len(action), device=DEVICE), action] = q_new

        # 4: Backpropagation (Retropropagation)
        # Gradient descent step to minimize the loss
        # between predicted and target Q-values
        # 1-Reset the gradients to zero before backpropagation
        # 2- Compute the loss between the predicted and target Q-values
        # 3- Compute the Backward pass to calculate the gradients
        # 4- Update the model's weights using the optimizer
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()

    def choose_action(self, state):
        if random.random() < self.epsilon:
            move_idx = random.randint(0, 3)
            action_text = self.actions[int(move_idx)]
            return action_text, move_idx
        return self.best_action(state)

    def best_action(self, state):
        """Returns the action with the highest Q-value for the given state."""
        state0 = torch.as_tensor(state,
                                 dtype=torch.float32,
                                 device=DEVICE).unsqueeze(0)
        with torch.no_grad():
            prediction = self.model(state0)
        move_idx = torch.argmax(prediction).item()
        action_text = self.actions[int(move_idx)]
        return action_text, move_idx

    def decay_epsilon(self):
        """Decays the exploration rate ε after each episode."""
        self.epsilon = max(
            self.epsilon_min,
            self.epsilon * self.epsilon_decay
        )

    def save_model(self, episodes):
        """Saves the model's state dictionary to a file."""
        if self.save_name and self.save_name != "q_table":
            self.model.save(f"{self.save_name}-{episodes}.pth")
        else:
            self.model.save(f"{self.name}-{episodes}.pth")
