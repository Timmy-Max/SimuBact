"""Module implements red bacteria class"""
import pygame
import random
import numpy as np
import torch
from pygame import Vector2

from bacteria import Bacteria
from genome import Genome
from pygame.sprite import Group
from pygame import display
from nn import NN


class RedBacteria(Bacteria):
    def __init__(
        self,
        screen: display,
        time_tick: float,
        load_weights: bool = False,
    ):
        """Initialization of red bacteria.

        Params:
            screen: screen for paint
            time_tick: time tick for to determine birth time
            load_weights: load weights for bacteria NN
        """
        super(Bacteria, self).__init__()

        self.type = "red"
        self.nn = NN((6, 60, 3))

        if load_weights:
            self.nn.load_state_dict(torch.load("weights/red_weights.pt"))
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
        new_bacteria = RedBacteria(screen, time_tick)
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
                    if bacteria.type == "green":
                        damage_received = max(
                            0, bacteria.genome.attack - self.genome.defense
                        )
                        damage_done = max(
                            0, self.genome.attack - bacteria.genome.defense
                        )
                        self.energy -= damage_received
                        if damage_done >= bacteria.energy:
                            self.energy += 20
                            self.score += 1
