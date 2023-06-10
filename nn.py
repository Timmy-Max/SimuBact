import torch
import torch.nn as nn

from typing import Any, Mapping


class NN(nn.Module):
    def __init__(self, sizes: tuple):
        """Initialization of NN.

        Params:
            size: sizes of layers
        """
        super().__init__()
        self.sizes = sizes
        self.nn = torch.nn.Sequential(
            nn.Linear(self.sizes[0], self.sizes[1]),
            nn.ReLU(),
            nn.Linear(self.sizes[1], self.sizes[1] // 2),
            nn.ReLU(),
            nn.Linear(self.sizes[1] // 2, sizes[2]),
            nn.Softmax(dim=0),
        )

    def feed_forward(self, inputs: tuple):
        """Function return"""
        with torch.no_grad():
            inputs = torch.FloatTensor(inputs)
        output = self.nn(inputs).detach().numpy()
        return output

    def update_weights(self, weights: Mapping[str, Any]):
        """Function copies the weights of another network to the current one

        Params:
            weights: weights of another bacteria network
        """
        self.nn.load_state_dict(state_dict=weights)
