import pygame
import random
import numpy as np

from genome import Genome
from nn import NN


class Bacteria(pygame.sprite.Sprite):

    def __init__(self, screen, bacteria_type, time_tick, load_weights=False):
        super(Bacteria, self).__init__()

        self.type = bacteria_type
        self.genome = Genome(4 * 8 + 8 * 3, self.type)

        screen_height = screen.get_height()
        screen_width = screen.get_width()
        initial_position = (random.randrange(0, screen_width, 1), random.randrange(0, screen_height, 1))

        self.screen = screen
        self.score = 0

        self.image_orig = pygame.image.load(f'Images/{self.type}_bacteria.png')
        self.image_orig = pygame.transform.scale(self.image_orig, self.genome.size)
        self.image = self.image_orig
        self.rect = self.image_orig.get_rect(center=initial_position)
        self.forward = pygame.math.Vector2(self.rect.topleft) - pygame.math.Vector2(self.rect.center)

        self.rot = random.randint(0, 360)
        self.rotate(self.rot)

        self.energy = 3
        self.velocity = pygame.math.Vector2(0.0, 0.0)

        self.age = 0
        self.birth_tick = time_tick / 1000
        self.last_rotate = time_tick
        self.nn = NN([3, 8, 3])

        if load_weights:
            self.genome.weights = list(np.load(f'Weights/{self.type}_weights.npz')['arr_0'])
            self.nn.update_weights(self.genome.weights, self.nn.sizes)

    def create_a_descendant(self, bacterias, screen, time_tick):
        new_bacteria = Bacteria(screen, self.type, time_tick)
        new_bacteria.genome = self.genome.mutate(0.5)
        new_bacteria.nn.update_weights(new_bacteria.genome.weights, self.nn.sizes)
        new_bacteria.rect.centerx = self.rect.centerx + (self.genome.size[0] // 2 + 3)
        new_bacteria.rect.centery = self.rect.centery
        bacterias.add(new_bacteria)

    def find_neighbors(self, bacterias, food):

        self_center = pygame.math.Vector2(self.rect.center)

        square_vision_radius = (self.genome.attack * 10.0 + 250.0) ** 2

        green_neighbours_count = 0
        green_neighbours_center = pygame.math.Vector2(0.0, 0.0)

        red_neighbours_count = 0
        red_neighbours_center = pygame.math.Vector2(0.0, 0.0)

        for bacteria in bacterias:
            if bacteria != self:
                bacteria_center = pygame.math.Vector2(bacteria.rect.center)
                getting_into_vision = (bacteria_center - self_center).length_squared()
                if getting_into_vision <= square_vision_radius:
                    if bacteria.type == 'green':
                        green_neighbours_count += 1
                        green_neighbours_center += bacteria_center
                    else:
                        red_neighbours_count += 1
                        red_neighbours_center += bacteria_center

        if green_neighbours_count == 0:
            green_neighbours_center = pygame.math.Vector2(0.0, 0.0)
        else:
            green_neighbours_center /= green_neighbours_count
            green_neighbours_center -= self_center

        if red_neighbours_count == 0:
            red_neighbours_center = pygame.math.Vector2(0.0, 0.0)
        else:
            red_neighbours_center /= red_neighbours_count
            red_neighbours_center -= self_center

        food_count = 0
        food_center = pygame.math.Vector2(0.0, 0.0)

        for food_i in food:
            food_i_center = pygame.math.Vector2(food_i.rect.center)
            getting_into_vision = (food_i_center - self_center).length_squared()
            if getting_into_vision <= square_vision_radius:
                food_count += 1
                food_center += food_i_center

        if food_count == 0:
            food_center = pygame.math.Vector2(0.0, 0.0)
        else:
            food_center /= food_count
            food_center -= self_center

        inputs = [green_neighbours_center.length(),
                  red_neighbours_center.length(),
                  food_center.length()]

        return [inputs, green_neighbours_center, red_neighbours_center, food_center]

    def update_age(self, time_tick):
        self.age += time_tick - self.birth_tick

    def update(self, screen, time_tick, bacterias, food):
        self.update_age(time_tick)
        neighbors_vectors = self.find_neighbors(bacterias, food)
        inputs = neighbors_vectors[0]
        outputs = self.nn.feed_forward(inputs)
        target = pygame.math.Vector2(0.0, 0.0)
        for i in range(3):
            direction = neighbors_vectors[1:][i]
            if direction.length() > 0:
                target += direction * outputs[i]

        self.move(target)
        self.boundary_check(screen)
        self.on_rect_enter(bacterias, food)

        if self.energy <= 0:
            self.kill()

        if self.energy >= 20:
            self.energy = 3
            self.create_a_descendant(bacterias, screen, time_tick)

        if self.age > 100000:
            self.kill()

    def on_rect_enter(self, bacterias, food):
        bacterias_collided = pygame.sprite.spritecollide(self, bacterias, False, False)
        for bacteria in bacterias_collided:
            if self.type == 'green' and bacteria.type == 'green':
                # self.velocity = 0.5 * bacteria.velocity
                # bacteria.velocity *= -0.5
                continue
            elif self.type == 'green' and bacteria.type == 'red':
                # self.velocity = bacteria.velocity * 0.5
                # bacteria.velocity *= -0.5
                damage_received = max(0, bacteria.genome.attack - self.genome.defense)
                damage_done = max(0, self.genome.attack - bacteria.genome.defense)
                self.energy -= damage_received
                if self.energy <= 0:
                    bacteria.energy += 17 - damage_done
                    bacteria.score += 1
            elif self.type == 'red' and bacteria.type == 'red':
                # self.velocity = 0.5 * bacteria.velocity
                # bacteria.velocity *= -0.5
                continue

        if self.type == 'green':
            food_collided = pygame.sprite.spritecollide(self, food, False, False)
            for food_i in food_collided:
                self.energy += 1
                self.score += 1
                food_i.kill()

    def rotate(self, angle):
        new_image = pygame.transform.rotate(self.image_orig, -angle - 90)
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect(center=old_center)

    def move(self, target):
        self.velocity += 0.05 * target * self.genome.speed

        radius, angle = self.velocity.as_polar()
        self.rotate(angle)

        self.rect.centerx += self.velocity.x
        self.rect.centery += self.velocity.y

    def boundary_check(self, screen):
        width = screen.get_width()
        height = screen.get_height()

        if self.rect.left <= 0:
            self.rect.left = 20
            self.velocity *= -1
        elif self.rect.right >= width:
            self.rect.right = width - 20
            self.velocity *= -1

        if self.rect.top <= 0:
            self.rect.top = 20
            self.velocity *= -1
        elif self.rect.bottom >= height:
            self.rect.bottom = height - 20
            self.velocity *= -1
