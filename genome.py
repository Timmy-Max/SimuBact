import random
import copy
import torch
import torch.nn as nn


class Genome:
    def __init__(self, bacteria_nn: nn.Module, bacteria_type: str):
        """Function initializes bacteria genome

        Params:
            bacteria_nn: neural network of bacteria
            bacteria_type: green or red type of bacteria
        """
        self.nn = bacteria_nn
        rand_size = random.randrange(1, 5)
        self.size = [15 + rand_size, 30 + rand_size]
        self.speed = 0.5 / ((self.size[0] + self.size[1]) / 2)

        if bacteria_type == "red":
            self.attack = 3 + random.randint(1, 5)
            self.defense = 1 + random.randint(1, 5)
        else:
            self.attack = 1 + random.randint(1, 5)
            self.defense = 3 + random.randint(1, 5)

    def mutate(self, prob: float = 0.5):
        """Function makes mutations in genome.

        Params:
            prob: probability to mutate
        """
        new_genome = copy.deepcopy(self)

        for param in self.nn.parameters():
            param.data += random.random() / 10 * torch.randn_like(param)

        if random.uniform(0.0, 1.0) < prob:
            new_genome.size[0] += self.size[0] + random.randint(-5, 5)
        if random.uniform(0.0, 1.0) < prob:
            new_genome.size[1] += self.size[1] + random.randint(-5, 5)
        new_genome.speed = 0.05 / ((new_genome.size[0] + new_genome.size[1]) / 2)
        if random.uniform(0.0, 1.0) < prob:
            new_genome.attack += random.randint(-2, 2)
        if random.uniform(0.0, 1.0) < prob:
            new_genome.defense += random.randint(-2, 2)

        return new_genome
