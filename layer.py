class Layer:

    def __init__(self, size, next_size, last_layer=False):
        self.size = size
        if last_layer:
            self.neurons = [0 for _ in range(size)]
            self.weights = [0 for _ in range(size)]
        else:
            self.neurons = [0 for _ in range(size)]
            self.weights = [[0 for _ in range(next_size)] for __ in range(size)]
