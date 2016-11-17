import graphics as gfx
import physics as phsx
import math

planets = []


def check_for_collision():
    was_changed = False
    for y in range(0, len(planets) - 1):
        for x in range(y, len(planets) - 1):
            if not was_changed:
                if phsx.planet_distance(planets[x], planets[x + 1]) <= planets[x].size:
                    # deletes a planet if it comes close to another planet
                    # and then adds up the masses into one big planet
                    gfx.undraw(window, planets[x+1])
                    gfx.undraw(window, planets[x])
                    planets[x].merge(planets.pop(x + 1))
                    was_changed = True

        #checks if planet out of the screen and destroys it if it is
        if not was_changed:
            if planets[y].x>window.size_x or planets[y].x<0 or \
                        planets[y].y > window.size_y or planets[y].y < 0:
                gfx.undraw(window,planets[y])
                planets.pop(y)
                was_changed=True


def attract_once():
    for y in range(0, len(planets) - 1):
        for x in range(y, len(planets) - 1):
            force = phsx.gravity_force(planets[x], planets[x + 1])

            planets[x].add_force(*force)
            planets[x + 1].add_force(-force[0], -force[1])


def default_setup():
    planets.append(phsx.Planet(window, 1, 500, 430))
    planets.append(phsx.Planet(window, 100, 500, 400))
    planets.append(phsx.Planet(window, 100, 500, 300))

    planets[0].add_force(7, 0)
    planets[1].add_force(340, 0)
    planets[2].add_force(-400, 0)

def place_planet(mouse_pos):
    planets.append(phsx.Planet(window, 1, mouse_pos[0], mouse_pos[1]))


window = gfx.Game_Window(1000, 500)
default_setup()

events = gfx.get_events()


planet_num = len(planets)
planet_num_temp = planet_num

while not events["was_closed"]:
    check_for_collision()
    attract_once()
    window.move_all_once(planets)

    events = gfx.get_events()

    if events["was_clicked"]:
        place_planet(events["mouse_pos"])

    planet_num_temp = planet_num
    planet_num = len(planets)
    if not planet_num==planet_num_temp:
        print planet_num
