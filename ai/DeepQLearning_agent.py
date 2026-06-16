import torch
import torch.optim as optim
import torch.nn as nn
import random

EPSILON = 1.0
EPSILON_DECAY = 0.9995
EPSILON_MIN = 0.01
LEARNING_RATE = 0.001
DISCOUNT = 0.9


class DeepQAgent:
    def __init__(self, model):
        self.lr = LEARNING_RATE
        self.gamma = DISCOUNT
        self.model = model
        self.epsilon = EPSILON
        self.epsilon_decay = EPSILON_DECAY
        self.epsilon_min = EPSILON_MIN
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()
        self.actions = ["UP", "DOWN", "LEFT", "RIGHT"]

    def learn(self, state, action, reward, next_state, done):
        # 1: Convert data to tensor
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        # this case for only on value
        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # 2: predicted Q values with current state
        pred = self.model(state)

        # 3: Compute the Q value with the Bellman's formula
        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx]
                Q_new += self.gamma * torch.max(self.model(next_state[idx]))

            # Updating the value for the choosen action
            target[idx][torch.argmax(action[idx]).item()] = Q_new

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
        state0 = torch.tensor(state, dtype=torch.float).unsqueeze(0)
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
