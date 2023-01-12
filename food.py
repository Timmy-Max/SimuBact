import random

import pygame
import random


class Food(pygame.sprite.Sprite):

    def __init__(self, screen):
        super(Food, self).__init__()
        self.screen = screen
        food_x = random.randint(0, screen.get_width())
        food_y = random.randrange(0, screen.get_height())
        self.image = pygame.image.load('Images/food_image.png')
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect(center=(food_x, food_y))
