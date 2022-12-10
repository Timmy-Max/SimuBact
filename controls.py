import pygame
import sys
from food import Food
import numpy as np


def events(bacterias):
    """events processing"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            green = None
            red = None
            for bacteria in bacterias:
                if bacteria.type == 'green':
                    green = bacteria
                elif bacteria.type == 'red':
                    red = bacteria
                if green != None and red != None:
                    break
            green_weights = green.genome.weights
            red_weights = red.genome.weights
            np.savez('Weights/green_weights', np.array(green_weights))
            np.savez('Weights/red_weights', np.array(red_weights))
            sys.exit()


def update(bg_color, screen, time_tick, bacterias, food):
    screen.fill(bg_color)
    food.draw(screen)

    if len(food) <= 750:
        [food.add(Food(screen)) for _ in range(250)]

    bacterias.update(screen, time_tick, bacterias, food)

    bacterias.draw(screen)
    pygame.display.flip()
