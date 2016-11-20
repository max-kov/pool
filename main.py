import graphics as gfx
import physics as phsx
import time
import pygame
from os import path

planets = []

def check_for_collision():
    # this is used to avoid errors after removing a planet
    was_changed = False

    for y in range(0, len(planets) - 1):
        for x in range(y, len(planets) - 1):
            if not was_changed:
                # this checks if the distance from 2 planets is less that their size
                if phsx.planet_distance(planets[x], planets[x + 1]) <= (planets[x].size + planets[y].size):
                    # deletes a planet if it comes close to another planet
                    # and then adds up the masses into one big planet
                    gfx.undraw(window, planets[x + 1])
                    gfx.undraw(window, planets[x])
                    planets[x].merge(planets.pop(x + 1))
                    was_changed = True
                    destruction_sound.play()

        # checks if put of the screen and destroys it if it is
        if not was_changed:
            if planets[y].x > window.size_x or planets[y].x < 0 or \
                            planets[y].y > window.size_y or planets[y].y < 0:
                gfx.undraw(window, planets[y])
                planets.pop(y)
                was_changed = True


def attract_once():
    for y in range(0, len(planets) - 1):
        for x in range(y + 1, len(planets)):
            force = phsx.gravity_force(planets[y], planets[x])

            planets[y].add_force(*force)
            planets[x].add_force(-force[0], -force[1])


def default_setup():
    planets.append(phsx.Planet(1, 500, 430))
    planets.append(phsx.Planet(100, 500, 400))
    planets.append(phsx.Planet(800, 500, 300))

    planets[0].add_force(7, 0)
    planets[1].add_force(340, 0)
    planets[2].add_force(-400, 0)


def place_planet():
    start_pos = pygame.mouse.get_pos()

    size = 1
    # function waits while user upresses the screen
    while pygame.mouse.get_pressed()[0]:
        pygame.event.get()
        # this draws the circle while the user still presses the button
        pygame.draw.circle(window.surface, (255, 255, 255), start_pos, int(size ** 0.3))
        window.update()
        # increases the size every 0.1 of a second
        size += 5
        time.sleep(0.1)

    end_pos = pygame.mouse.get_pos()

    planets.append(phsx.Planet(size, start_pos[0], start_pos[1]))
    planets[len(planets) - 1].add_force(size * (end_pos[0] - start_pos[0]) / 10,
                                        size * (end_pos[1] - start_pos[1]) / 10)


if __name__ == "__main__":
    window = gfx.game_window(1000, 500)

    window.main_menu()

    selection_sound = pygame.mixer.Sound(path.join('resources', 'reload.ogg'))
    selection_sound.play()
    destruction_sound = pygame.mixer.Sound(path.join('resources', 'boom.wav'))

    default_setup()

    events = gfx.get_events()

    while not events["was_closed"]:
        check_for_collision()
        attract_once()
        window.move_all_once(planets)

        events = gfx.get_events()

        if events["was_clicked"]:
            place_planet()
