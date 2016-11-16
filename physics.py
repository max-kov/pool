import math, gfx

#works only in one dimension
def gravity_force(pl1,pl2):
    dist_x = (pl1.x-pl2.x)
    dist_y = (pl1.y-pl2.y)
    # using pythaoreas to calculate the range between planets
    dist = math.sqrt(dist_x**2 + dist_y**2)
    force = (pl1.mass*pl2.mass)/(dist**2)
    force_x = force*(dist_x/dist)
    force_y = force*(dist_y/dist)
    return -force_x, -force_y