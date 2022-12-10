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

    bacterias = Group()
    [bacterias.add(Bacteria(screen, 'green', start_tick, True)) for _ in range(amount_of_green)]
    [bacterias.add(Bacteria(screen, 'red', start_tick, True)) for _ in range(amount_of_red)]

    food = Group()
    [food.add(Food(screen)) for _ in range(amount_of_food)]

    clock = pygame.time.Clock()
    fps = 30

    while True:
        clock.tick(fps)
        current_tick = pygame.time.get_ticks() / 1000
        controls.events(bacterias)
        controls.update(bg_color, screen, current_tick, bacterias, food)


if __name__ == '__main__':
    width, height = 1500, 800
    title = 'BactSimu'
    bg_color = (255, 255, 255)
    amount_of_food = 1000
    amount_of_green = 20
    amount_of_red = 5
    update(width, height, title, bg_color, amount_of_food, amount_of_green, amount_of_red)
