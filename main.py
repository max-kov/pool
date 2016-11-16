import graphics as gfx
import physics as phsx

planets = []

def attract_once():
    for y in range(0,len(planets)-1):
        for x in range(y,len(planets)-1):
            force = phsx.gravity_force(planets[x],planets[x+1])

            planets[x].add_force(*force)
            planets[x+1].add_force(-force[0],-force[1])


def setup_default():
    planets.append(phsx.Planet(window, 1, 500, 550))
    planets.append(phsx.Planet(window, 80, 500, 500))
    planets.append(phsx.Planet(window, 80, 300, 300))

    planets[0].add_force(0.9, -0.6)
    planets[1].add_force(-0.6, 0.6)



window = gfx.Game_Window(1000, 1000)
setup_default()

while 1:
    attract_once()
    window.move_all_once(planets)
