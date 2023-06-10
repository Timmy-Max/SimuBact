import pygame
import sys
import torch

from pygame import display
from food import Food
from pygame.sprite import Group


def save_weights(bacterias: Group):
    """Function implements saving nn's weights of best green and red bacteria.

    Params:
        bacterias: group of current bacterias
    """
    green = []
    red = []
    green_max_score = 0
    red_max_score = 0
    for bacteria in bacterias:
        if bacteria.type == "green":
            if bacteria.score >= green_max_score:
                green_max_score = bacteria.score
                green = bacteria
        elif bacteria.type == "red":
            if bacteria.score >= red_max_score:
                red_max_score = bacteria.score
                red = bacteria

    if green != [] and red != []:
        green_nn = green.nn
        red_nn = red.nn
        torch.save(green_nn.state_dict(), "weights/green_weights.pt")
        torch.save(red_nn.state_dict(), "weights/red_weights.pt")


def events(bacterias: Group, save=False):
    """Function handles events

    Params:
        bacterias: group of current bacterias
        save: saving
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if save and len(bacterias) != 0:
                save_weights(bacterias)
            sys.exit()


def update(
    bg_color: tuple[int, int, int],
    screen: display,
    time_tick: float,
    bacterias: Group,
    food: Group,
):
    """Function implements updating  game

    Params:
        bg_color: background color
        screen: display for paint
        time_tick: current time tick
        bacterias: group of current bacterias
        food: group of current food
    """
    screen.fill(bg_color)
    food.draw(screen)

    if len(food) < 1500:
        [food.add(Food(screen)) for _ in range(max(0, 1500 - len(food)))]

    bacterias.update(screen, time_tick, bacterias, food)

    bacterias.draw(screen)
    pygame.display.flip()
