from layer import Layer
import random
import copy


class NN:
    def __init__(self, sizes):
        self.sizes = sizes
        sizes_length = len(sizes)
        self.layers = []

        for i in range(len(sizes)):
            next_size = 0
            if i < sizes_length - 1:
                next_size = sizes[i + 1]
                self.layers.append(Layer(sizes[i], next_size))
                for j in range(sizes[i]):
                    for k in range(next_size):
                        self.layers[i].weights[j][k] = random.uniform(-1.0, 1.0)
            else:
                self.layers.append(Layer(sizes[i], 0, True))
                for k in range(sizes[i]):
                    self.layers[i].weights[k] = random.uniform(-1.0, 1.0)

    def feed_forward(self, inputs):
        self.layers[0].neurons = copy.deepcopy(inputs)
        layers_count = len(self.layers)
        for i in range(1, layers_count):
            min_ = 0.0
            if i == layers_count - 1:
                min_ = -1.0
            layer_prev = self.layers[i - 1]
            layer_next = self.layers[i]
            for j in range(layer_next.size):
                layer_next.neurons[j] = 0
                for k in range(layer_prev.size):
                    layer_next.neurons[j] += layer_prev.neurons[k] * layer_prev.weights[k][j]
                layer_next.neurons[j] = min(1.0, max(min_, layer_next.neurons[j]))

        return self.layers[layers_count - 1].neurons

    def update_weights(self, weights, sizes):
        for i in range(sizes[0]):
            for j in range(sizes[1]):
                self.layers[0].weights[i][j] = weights[i + j * sizes[0]]

        for i in range(sizes[1]):
            for j in range(sizes[2]):
                self.layers[1].weights[i][j] = weights[i + j * sizes[1] + sizes[0] * sizes[1]]