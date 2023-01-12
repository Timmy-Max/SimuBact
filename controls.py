import pygame
import sys
from food import Food
import numpy as np


def save_weights(bacterias):
    green = []
    red = []
    green_max_score = 0
    red_max_score = 0
    for bacteria in bacterias:
        if bacteria.type == 'green':
            if bacteria.score >= green_max_score:
                green_max_score = bacteria.score
                green = bacteria
        elif bacteria.type == 'red':
            if bacteria.score >= red_max_score:
                red_max_score = bacteria.score
                red = bacteria

    if green != [] and red != []:
        green_weights = green.genome.weights
        red_weights = red.genome.weights
        np.savez('Weights/green_weights', np.array(green_weights))
        np.savez('Weights/red_weights', np.array(red_weights))


def events(bacterias, save=False):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if save and bacterias != []:
                save_weights(bacterias)
            sys.exit()


def update(bg_color, screen, time_tick, bacterias, food, green_bacterias, red_bacterias):
    screen.fill(bg_color)
    food.draw(screen)

    if pygame.time.get_ticks() % 50 == 0:
        [food.add(Food(screen)) for _ in range(50)]

    bacterias.update(screen, time_tick, bacterias, food)

    bacterias.draw(screen)
    pygame.display.flip()
