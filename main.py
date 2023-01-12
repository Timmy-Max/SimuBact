import pygame
import controls
from pygame.sprite import Group
from bacteria import Bacteria
from food import Food


def update(width, height, title, bg_color, amount_of_food, amount_of_green, amount_of_red):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)

    start_tick = pygame.time.get_ticks()

    save = True
    load = True

    bacterias = Group()
    green_bacterias = Group()
    red_bacterias = Group()
    for _ in range(amount_of_green):
        green_bacteria = Bacteria(screen, 'green', start_tick, load)
        bacterias.add(green_bacteria)
        green_bacterias.add(green_bacteria)

    for _ in range(amount_of_red):
        red_bacteria = Bacteria(screen, 'red', start_tick, load)
        bacterias.add(red_bacteria)
        red_bacterias.add(red_bacteria)

    food = Group()
    [food.add(Food(screen)) for _ in range(amount_of_food)]

    clock = pygame.time.Clock()
    fps = 60

    while True:
        clock.tick(fps)
        current_tick = pygame.time.get_ticks() / 1000
        controls.events(bacterias, save)
        controls.update(bg_color, screen, current_tick, bacterias, food, green_bacterias, red_bacterias)


if __name__ == '__main__':
    width, height = 800, 800
    title = 'SimuBact'
    bg_color = (255, 255, 255)
    amount_of_food = 500
    amount_of_green = 25
    amount_of_red = 8
    update(width, height, title, bg_color, amount_of_food, amount_of_green, amount_of_red)
