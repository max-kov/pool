import math

def planet_distance(pl1,pl2):
    # using pythaoreas to calculate the range between planets
    dist_x = (pl1.x-pl2.x)
    dist_y = (pl1.y-pl2.y)
    return math.sqrt(dist_x**2 + dist_y**2)

#works only in one dimension
def gravity_force(pl1,pl2):
    dist_x = (pl1.x-pl2.x)
    dist_y = (pl1.y-pl2.y)
    dist = planet_distance(pl1,pl2)
    #using newtonian model for gravitational attraction
    force = (pl1.mass*pl2.mass)/(dist**2)
    force_x = force*(dist_x/dist)
    force_y = force*(dist_y/dist)
    return -force_x, -force_y