import graphics as gfx
import physics as phsx
import time
import pygame
from os import path
from random import randint

planets = []


def check_for_collision():
    # this is used to avoid errors after removing a planet
    was_changed = False

    for y in range(0, len(planets)):
        for x in range(y, len(planets)):
            if not was_changed and not x == y:
                # this checks if the distance from 2 planets is less that their size
                if phsx.planet_distance(planets[y], planets[x]) < (planets[x].size + planets[y].size):
                    # deletes a planet if it comes close to another planet
                    # and then adds up the masses into one big planet
                    gfx.undraw(window, planets[y])
                    gfx.undraw(window, planets[x])
                    if planets[x].is_moveable:
                        temp = x
                        x = y
                        y = temp
                    planets[y].merge(planets.pop(x))
                    was_changed = True
                    destruction_sound.play()

        # checks if put of the screen and destroys it if it is
        if not was_changed:
            if planets[y].x - planets[y].size > window.size_x or planets[y].x + planets[y].size < 0 or \
                                    planets[y].y - planets[y].size > window.size_y or planets[y].y + planets[
                y].size < 0:
                gfx.undraw(window, planets[y])
                planets.pop(y)
                was_changed = True


def attract_once():
    for y in range(0, len(planets)):
        for x in range(y, len(planets)):
            if not x == y:
                force = phsx.gravity_force(planets[y], planets[x])
                if not planets[y].is_moveable:
                    planets[y].add_force(*force)
                if not planets[x].is_moveable:
                    planets[x].add_force(-force[0], -force[1])


def default_setup():
    planets.append(phsx.Planet(10, 580, 250))
    planets.append(phsx.Planet(10, 630, 250))
    planets.append(phsx.Planet(10, 690, 250))
    planets.append(phsx.Planet(10, 790, 250))

    planets.append(phsx.Planet(800, 500, 250, is_moveable=True))

    planets[0].add_force(0, 10)
    planets[1].add_force(0, 10)
    planets[2].add_force(0, 10)
    planets[3].add_force(0, 10)
    planets[4].add_force(0, 10)


def add_random_planet(window):
    side = randint(1, 4)
    size = randint(1, 1000)

    x = 0
    y = 0
    dx = 0
    dy = 0

    if side == 1:
        x = 0
        y = randint(100, window.size_y - 100)
        dx = randint(1, 5) * size / 3
        dy = randint(-5, 5) * size / 3
    elif side == 2:
        x = window.size_x
        y = randint(100, window.size_y - 100)
        dx = randint(-5, -1) * size / 3
        dy = randint(-5, 5) * size / 3
    elif side == 3:
        x = randint(100, window.size_x - 100)
        y = 0
        dx = randint(-5, 5) * size / 3
        dy = randint(1, 5) * size / 3
    elif side == 4:
        x = randint(100, window.size_x - 100)
        y = window.size_y
        dx = randint(-5, 5) * size / 3
        dy = randint(-5, -1) * size / 3

    planets.append(phsx.Planet(size, x, y))
    planets[len(planets) - 1].add_force(dx, dy)


def random_setup(window):
    for x in range(0, 10):
        add_random_planet(window)


def place_planet():
    start_pos = pygame.mouse.get_pos()
    is_right_click = bool(pygame.mouse.get_pressed()[2])

    size = 1
    # function waits while user unpresses the screen
    while pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
        pygame.event.get()
        # this draws the circle while the user still presses the button
        pygame.draw.circle(window.surface, (255, 255, 255), start_pos, int(size ** 0.3))
        window.update()
        # increases the size every 0.1 of a second
        size += 5
        time.sleep(0.1)

    end_pos = pygame.mouse.get_pos()
    if is_right_click:
        planets.append(phsx.Planet(size, start_pos[0], start_pos[1], is_moveable=True))
    else:
        planets.append(phsx.Planet(size, start_pos[0], start_pos[1]))
        planets[len(planets) - 1].add_force(size * (end_pos[0] - start_pos[0]) / 10,
                                            size * (end_pos[1] - start_pos[1]) / 10)


if __name__ == "__main__":
    window = gfx.game_window(1000, 500)

    selected = window.main_menu()

    selection_sound = pygame.mixer.Sound(path.join('resources', 'reload.ogg'))
    selection_sound.play()
    destruction_sound = pygame.mixer.Sound(path.join('resources', 'boom.wav'))

    if selected == 1:
        default_setup()
    elif selected == 2:
        random_setup(window)

    events = gfx.get_events()

    while not events["was_closed"]:
        check_for_collision()
        attract_once()
        window.move_all_once(planets)

        events = gfx.get_events()

        if events["was_clicked"]:
            place_planet()
        if len(planets) < 5 and selected == 2:
            add_random_planet(window)
