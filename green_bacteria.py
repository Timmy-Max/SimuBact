"""Module implements green bacteria class"""
import pygame
import random
import torch

from bacteria import Bacteria
from genome import Genome
from pygame.sprite import Group
from pygame import display
from nn import NN


class GreenBacteria(Bacteria):
    def __init__(
        self,
        screen: display,
        time_tick: float,
        load_weights: bool = False,
    ):
        """Initialization of green bacteria.

        Params:
            screen: screen for paint
            time_tick: time tick for to determine birth time
            load_weights: load weights for bacteria NN
        """
        super(Bacteria, self).__init__()

        self.type = "green"
        self.nn = NN((6, 60, 3))

        if load_weights:
            self.nn.load_state_dict(torch.load("weights/green_weights.pt"))
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
        new_bacteria = GreenBacteria(screen, time_tick)
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

    def on_rect_enter(self, bacterias: Group, food: Group):
        """Function handles collisions.

        Params:
            bacterias: group of current bacterias
            food: group of current food
        """
        for bacteria in bacterias:
            if self.rect.colliderect(bacteria.rect):
                if bacteria is not self:
                    if bacteria.type == "red":
                        damage_received = max(
                            0, bacteria.genome.attack - self.genome.defense
                        )
                        self.energy -= damage_received

                food_collided = pygame.sprite.spritecollide(self, food, dokill=False)
                for food_i in food_collided:
                    self.energy += 1
                    self.score += 1
                    food_i.kill()
