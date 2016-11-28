import graphics as gfx
import physics as phsx
import time
import pygame
from os import path
from random import randint

planets = []
window = gfx.game_window(1000, 500)

def check_for_collision():
    # this is used to avoid errors after removing a planet
    was_changed = False

    for counter1 in range(0, len(planets)):
        if not was_changed:
            pl1 = planets[counter1]

        for counter2 in range(counter1, len(planets)):
            if not was_changed and not counter2 == counter1:

                pl2 = planets[counter2]

                # this checks if the distance from 2 planets is less that their size
                if phsx.planet_distance(pl1, pl2) < (pl2.size + pl1.size):
                    # deletes a planet if it comes close to another planet
                    # and then adds up the masses into one big planet
                    gfx.undraw(window, pl1)
                    gfx.undraw(window, pl2)
                    if pl2.not_moveable:
                        temp = counter2
                        counter2 = counter1
                        counter1 = temp
                    pl1.merge(planets.pop(counter2))
                    was_changed = True
                    destruction_sound.play()

        # checks if put of the screen and destroys it if it is
        if not was_changed:
            if pl1.x - pl1.size > window.size_x or pl1.x + pl1.size < 0 or \
                pl1.y - pl1.size > window.size_y or pl1.y + pl1.size < 0:
                gfx.undraw(window, pl1)
                planets.pop(counter1)
                was_changed = True

def check_for_collision_bouncy():
    for counter1 in range(0, len(planets)):

        pl1 = planets[counter1]

        for counter2 in range(counter1, len(planets)):
            pl2 = planets[counter2]
            if not counter1==counter2:
                if phsx.collision_test(pl1,pl2):
                    phsx.collide_bouncy(pl1, pl2)


        if pl1.x + pl1.size > window.size_x or pl1.x - pl1.size<0:
            if (pl1.x + pl1.size > window.size_x and not pl1.dx < 0) or (
                                        pl1.x - pl1.size < 0 and not pl1.dx > 0):
                pl1.set_vector(-pl1.dx, pl1.dy)
        if pl1.y + pl1.size > window.size_y or pl1.y - pl1.size<0:
            if (pl1.y + pl1.size > window.size_y and not pl1.dy<0) or (pl1.y - pl1.size<0 and not pl1.dy>0):
                pl1.set_vector(pl1.dx, -pl1.dy)


def attract_once():
    for y in range(0, len(planets)):
        for x in range(y, len(planets)):
            if not x == y:
                force = phsx.gravity_force(planets[y], planets[x])
                if not planets[y].not_moveable:
                    planets[y].add_force(*force)
                if not planets[x].not_moveable:
                    planets[x].add_force(-force[0], -force[1])


def default_setup():
    planets.append(phsx.Planet(15, 580, 250))
    planets.append(phsx.Planet(15, 630, 250))
    planets.append(phsx.Planet(15, 690, 250))
    planets.append(phsx.Planet(15, 790, 250))

    planets.append(phsx.Planet(800, 500, 250, not_moveable=True))

    planets[0].set_vector(0, 1.5)
    planets[1].set_vector(0, 1)
    planets[2].set_vector(0, 1)
    planets[3].set_vector(0, 1)


def add_random_planet():
    side = randint(1, 4)
    size = randint(1, 500)

    x = 0
    y = 0
    dx = 0
    dy = 0

    if side == 1:
        x = 0
        y = randint(size, window.size_y )
        dx = randint(1, 5)
        dy = randint(-5, 5)
    elif side == 2:
        x = window.size_x
        y = randint(size+1, window.size_y )
        dx = randint(-5, -1)
        dy = randint(-5, 5)
    elif side == 3:
        x = randint(size, window.size_x)
        y = 0
        dx = randint(-5, 5)
        dy = randint(1, 5)
    elif side == 4:
        x = randint(size, window.size_x)
        y = window.size_y
        dx = randint(-5, 5)
        dy = randint(-5, -1)

    planets.append(phsx.Planet(size, x, y))
    planets[len(planets) - 1].set_vector(dx/5, dy/5)


def random_setup():
    for x in range(0, 10):
        add_random_planet()

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
        planets.append(phsx.Planet(size, start_pos[0], start_pos[1],not_moveable=True))
    else:
        planets.append(phsx.Planet(size, start_pos[0], start_pos[1]))
        planets[len(planets) - 1].set_vector(size * (end_pos[0] - start_pos[0]) / 500,
                                            size * (end_pos[1] - start_pos[1]) / 500)


def place_planet_bouncy():
    start_pos = pygame.mouse.get_pos()

    size = 1
    # function waits while user unpresses the screen
    while pygame.mouse.get_pressed()[0]:
        pygame.event.get()
        # this draws the circle while the user still presses the button
        pygame.draw.circle(window.surface, (255, 255, 255), start_pos, int(size))
        window.update()
        # increases the size every 0.1 of a second
        size += 5
        time.sleep(0.1)

    end_pos = pygame.mouse.get_pos()
    planets.append(phsx.Planet(size, start_pos[0], start_pos[1], is_bouncy=True))
    planets[len(planets) - 1].set_vector(size * (end_pos[0] - start_pos[0]) / 500,
                                            size * (end_pos[1] - start_pos[1]) / 500)


if __name__ == "__main__":
    selected = window.main_menu()

    selection_sound = pygame.mixer.Sound(path.join('resources', 'reload.ogg'))
    selection_sound.play()
    destruction_sound = pygame.mixer.Sound(path.join('resources', 'boom.wav'))

    events = gfx.get_events()

    if selected == 1:
        #normal mode selected in menu
        default_setup()

        while not events["was_closed"]:
            check_for_collision()
            attract_once()
            window.move_all_once(planets)

            events = gfx.get_events()

            if events["was_clicked"]:
                place_planet()

    elif selected == 2:
        #random stars selected in menu
        random_setup()

        while not events["was_closed"]:
            check_for_collision()
            attract_once()
            window.move_all_once(planets)

            events = gfx.get_events()

            if events["was_clicked"]:
                place_planet()
            if len(planets) < 10:
                add_random_planet()

    elif selected == 3:
        #bouncy balls mode selected in menu

        planets.append(phsx.Planet(40, 300, 300, is_bouncy=True))
        planets[0].set_vector(-1, 0.01)

        planets.append(phsx.Planet(10, 400, 290, is_bouncy=True))
        planets[1].set_vector(-2, 0)

        while not events["was_closed"]:
            check_for_collision_bouncy()
            window.move_all_once(planets)

            events = gfx.get_events()

            if events["was_clicked"]:
                place_planet_bouncy()

    pygame.quit()