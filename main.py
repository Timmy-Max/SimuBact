import pygame
import controls
from pygame.sprite import Group
from food import Food
from green_bacteria import GreenBacteria
from red_bacteria import RedBacteria

FPS = 120


def update(
    s_width: int,
    s_height: int,
    s_title: str,
    s_bg_color: tuple,
    amount_food: int,
    amount_green: int,
    amount_red: int,
    load_w: bool,
    save_w: bool,
):
    """Function creates screen and init population of bacterias and food. Then update screen.

    Params:
        s_width: screen width
        s_height: screen height
        title: title of screen
        bg_color: color of background
        amount_of_food: amount of food in the screen
        amount_of_green: amount of green bacterias
        amount_of_red: amount of red bacterias
        load_w: loading weights for bacterias from previous episode
        save_w: saving weights for bacterias after episode
    """
    pygame.init()
    screen = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption(s_title)

    start_tick = pygame.time.get_ticks()

    bacterias = Group()
    for _ in range(amount_green):
        green_bacteria = GreenBacteria(screen, start_tick, load_w)
        bacterias.add(green_bacteria)

    for _ in range(amount_red):
        red_bacteria = RedBacteria(screen, start_tick, load_w)
        bacterias.add(red_bacteria)

    food = Group()
    [food.add(Food(screen)) for _ in range(amount_food)]

    clock = pygame.time.Clock()

    while True:
        clock.tick(FPS)
        current_tick = pygame.time.get_ticks() / 1000
        controls.events(bacterias, save_w)
        controls.update(
            s_bg_color,
            screen,
            current_tick,
            bacterias,
            food,
        )


if __name__ == "__main__":
    width, height = 800, 800
    title = "SimuBact"
    bg_color = (255, 255, 255)
    amount_of_food = 1500
    amount_of_green = 10
    amount_of_red = 3
    load = True
    save = True
    update(
        width,
        height,
        title,
        bg_color,
        amount_of_food,
        amount_of_green,
        amount_of_red,
        load,
        save,
    )
