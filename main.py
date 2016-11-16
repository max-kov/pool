import graphics as gfx
import physics as phsx
import math

planets = []


def destroy_if_close():
    for y in range(0, len(planets) - 1):
        for x in range(y, len(planets) - 1):
            if phsx.planet_distance(planets[x], planets[x + 1]) < planets[x].size:
                # deletes a planet if it comes close to another planet
                # and then adds up the masses into one big planet
                planets[x].merge(planets.pop(x + 1))


def attract_once():
    for y in range(0, len(planets) - 1):
        for x in range(y, len(planets) - 1):
            force = phsx.gravity_force(planets[x], planets[x + 1])

            planets[x].add_force(*force)
            planets[x + 1].add_force(-force[0], -force[1])


def setup_default():
    planets.append(phsx.Planet(window, 1, 500, 430))
    planets.append(phsx.Planet(window, 100, 500, 400))
    planets.append(phsx.Planet(window, 800, 500, 300))

    planets[0].add_force(7, 0)
    planets[1].add_force(340, 0)
    planets[2].add_force(-400, 0)


window = gfx.Game_Window(1000, 500)
setup_default()

while 1:
    destroy_if_close()
    attract_once()
    window.move_all_once(planets)
