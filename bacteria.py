"""Module implements bacteria class"""
import pygame
import random
import torch

from genome import Genome
from pygame.sprite import Group
from pygame import display
from nn import NN


class Bacteria(pygame.sprite.Sprite):
    def __init__(
        self,
        screen: display,
        bacteria_type: str,
        time_tick: float,
        load_weights: bool = False,
    ):
        """Initialization of bacteria.

        Params:
            screen: screen for paint
            bacteria_type: red or green type of bacteria
            time_tick: time tick for to determine birth time
            load_weights: load weights for bacteria NN
        """
        super(Bacteria, self).__init__()

        self.type = bacteria_type
        self.nn = NN((6, 20, 3))

        if load_weights:
            self.nn.load_state_dict(torch.load(f"weights/{self.type}_weights.pt"))
        self.genome = Genome(self.nn, self.type)

        screen_height = screen.get_height()
        screen_width = screen.get_width()
        initial_position = (
            random.randrange(0, screen_width, 1),
            random.randrange(0, screen_height, 1),
        )

        self.screen = screen
        self.score = 0

        self.image_orig = pygame.image.load(f"images/{self.type}_bacteria.png")
        self.image_orig = pygame.transform.scale(self.image_orig, self.genome.size)
        self.image = self.image_orig
        self.rect = self.image_orig.get_rect(center=initial_position)
        self.forward = pygame.math.Vector2(self.rect.topleft) - pygame.math.Vector2(
            self.rect.center
        )
        self.rot = random.randint(0, 360)
        self.rotate(self.rot)

        self.energy = 3
        self.velocity = pygame.math.Vector2(0.0, 0.0)

        self.age = 0
        self.birth_tick = time_tick / 1000
        self.last_rotate = time_tick

    def create_descendant(self, bacterias: Group, screen: display, time_tick: float):
        """Creates descendant of current bacteria.

        Params:
            bacterias: group of bacterias to insert new bacteria
            screen: screen for paint
            time_tick: time tick to determine birth time
        """
        new_bacteria = Bacteria(screen, self.type, time_tick)
        new_bacteria.genome = self.genome.mutate()
        new_bacteria.nn = new_bacteria.genome.nn
        new_bacteria_x = self.rect.centerx + (self.genome.size[0] // 2 + 3)
        new_bacteria_y = self.rect.centery
        new_bacteria.image_orig = pygame.transform.scale(
            self.image_orig, self.genome.size
        )
        new_bacteria.image = new_bacteria.image_orig
        new_bacteria.rect = new_bacteria.image_orig.get_rect(
            center=(new_bacteria_x, new_bacteria_y)
        )
        bacterias.add(new_bacteria)

    def find_neighbors(
        self, bacterias: Group, food: Group
    ) -> tuple[float, float, float, float, float, float]:
        """Function computes mass centers of green, red bacterias and food.

        Params:
            bacterias: all current bacterias
            food: all current food

        Returns:
            tuple: inputs for bacteria NN
        """
        self_center = pygame.math.Vector2(self.rect.center)

        vision_radius = self.genome.attack * 10.0 + 250.0

        green_neighbours_count = 0
        green_neighbours_center = pygame.math.Vector2(0.0, 0.0)

        red_neighbours_count = 0
        red_neighbours_center = pygame.math.Vector2(0.0, 0.0)

        for bacteria in bacterias:
            if bacteria is not self:
                bacteria_center = pygame.math.Vector2(bacteria.rect.center)
                getting_into_vision = (bacteria_center - self_center).length()
                if getting_into_vision <= vision_radius:
                    if bacteria.type == "green":
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
            green_len = green_neighbours_center.length()
            if green_len != 0:
                green_neighbours_center /= green_len

        if red_neighbours_count == 0:
            red_neighbours_center = pygame.math.Vector2(0.0, 0.0)
        else:
            red_neighbours_center /= red_neighbours_count
            red_neighbours_center -= self_center
            red_len = red_neighbours_center.length()
            if red_len != 0:
                red_neighbours_center /= red_len

        food_count = 0
        food_center = pygame.math.Vector2(0.0, 0.0)

        for food_i in food:
            food_i_center = pygame.math.Vector2(food_i.rect.center)
            getting_into_vision = (food_i_center - self_center).length()
            if getting_into_vision <= vision_radius:
                food_count += 1
                food_center += food_i_center

        if food_count == 0:
            food_center = pygame.math.Vector2(0.0, 0.0)
        else:
            food_center /= food_count
            food_center -= self_center
            food_len = food_center.length()
            if food_len != 0:
                food_center /= food_len

        nn_inputs = (
            green_neighbours_center[0],
            green_neighbours_center[1],
            red_neighbours_center[0],
            red_neighbours_center[1],
            food_center[0],
            food_center[1],
        )

        return nn_inputs

    def update_age(self, time_tick: float):
        """Function update lifetime of bacteria.

        Params:
           time_tick: current time_tick
        """
        self.age += time_tick - self.birth_tick

    def update(self, screen: display, time_tick: float, bacterias: Group, food: Group):
        """Function update state of bacteria.

        Params:
            screen: display for paint
            time_tick: current time_tick
            bacterias: group of current bacterias
            food: group of current food
        """
        self.update_age(time_tick)
        inputs = self.find_neighbors(bacterias, food)
        outputs = self.nn.feed_forward(inputs)
        trg_vectors = []
        for i in range(0, 5, 2):
            trg_vectors.append(pygame.math.Vector2(inputs[i], inputs[i + 1]))
        target = pygame.math.Vector2(0.0, 0.0)
        for i in range(3):
            target += trg_vectors[i] * outputs[i]
        target_len = target.length()
        if target_len == 0:
            target = pygame.math.Vector2(random.random(), random.random())
        target /= target_len

        self.move(target)
        self.boundary_check(screen)
        self.on_rect_enter(bacterias, food)

        if self.energy <= 0:
            self.kill()

        if self.energy >= 20:
            self.energy = 3
            self.create_descendant(bacterias, screen, time_tick)

        if self.age > 10000:
            self.kill()

    def on_rect_enter(self, bacterias: Group, food: Group):
        """Creates descendant of current bacteria.

        Params:
            bacterias: group of bacterias to insert new bacteria
            screen: screen for paint
            time_tick: time tick to determine birth time
        """
        pass

    def rotate(self, angle: float):
        """Bacteria rotation function.

        Params:
            angle: angle of rotation
        """
        new_image = pygame.transform.rotate(self.image_orig, -angle - 90)
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect(center=old_center)

    def move(self, target: pygame.math.Vector2):
        """Bacteria rotation function.

        Params:
            target: direction of movement
        """
        self.velocity += target * self.genome.speed

        radius, angle = self.velocity.as_polar()
        self.rotate(angle)

        self.rect.centerx += self.velocity.x
        self.rect.centery += self.velocity.y

    def boundary_check(self, screen):
        """Function does not allow bacteria to escape from the screen.

        Params:
            screen: screen for paint
        """
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
