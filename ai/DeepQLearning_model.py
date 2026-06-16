import torch
import torch.nn as nn
import torch.nn.functional as F
import os


class DeepQModel(nn.Module):
    def __init__(self,
                 input_size: int,
                 hidden_size_1: int,
                 hidden_size_2: int,
                 output_size: int,
                 load_name: str | None = None):
        """A simple feedforward neural network for Deep Q-Learning.

        Args:
            input_size (int): Number of input features (state size).
            hidden_size_1 (int): Number of neurons in the first hidden layer.
            hidden_size_2 (int): Number of neurons in the second hidden layer.
            output_size (int): Number of output actions (action size).
        """
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size_1)
        self.linear2 = nn.Linear(hidden_size_1, hidden_size_2)
        self.linear3 = nn.Linear(hidden_size_2, output_size)
        if load_name:
            self.load(load_name)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = F.relu(self.linear2(x))
        x = self.linear3(x)
        return x

    def save(self, file_name='dqn_model.pth'):
        model_folder_path = './models'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

    def load(self, file_name='dqn_model.pth'):
        model_folder_path = './models'
        file_name = os.path.join(model_folder_path, file_name)
        if os.path.exists(file_name):
            self.load_state_dict(torch.load(file_name))
