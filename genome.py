import random
import copy


class Genome:

    def __init__(self, size, type):
        self.weights = []
        for i in range(size):
            self.weights.append(random.uniform(-1.0, 1.0))

        rand_size = random.randrange(1, 15)
        self.size = [5 + rand_size, 12.5 + rand_size * 2.5]
        self.speed = 0.1 / ((self.size[0] + self.size[1]) / 2)
        self.defense = 1 + random.randint(1, 5)
        if type == 'red':
            self.attack = 3 + random.randint(1, 5)
        else:
            self.attack = 1 + random.randint(1, 5)

    def mutate(self, value):
        new_genome = copy.deepcopy(self)

        for i in range(len(new_genome.weights)):
            if random.uniform(0.0, 1.0) < 0.1:
                new_genome.weights[i] += random.uniform(-value, value)

        new_genome.size[0] += self.size[0] + random.randint(-5, 5)
        new_genome.size[1] += self.size[1] + random.randint(-5, 5)
        new_genome.speed = 1 / ((new_genome.size[0] + new_genome.size[1]) / 2)
        new_genome.attack += random.randint(-1, 1)
        new_genome.defense += random.randint(-1, 1)

        return new_genome


    # def __init__(self, bacteria):
    #     self.skills = copy.deepcopy(bacteria.genome.skills)
    #     self.weights = copy.deepcopy(bacteria.genome.weights)
