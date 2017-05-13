import math

import numpy as np
import pygame

# window settings
resolution = np.array([1000, 500])
table_margin = 60
table_side_color = (200, 200, 0)
table_color = (0, 100, 0)
hole_radius = 22
window_caption = "Pool"
fps_limit = 100
# cue settings
cue_color = (100, 100, 100)
cue_hit_power = 3
cue_length = 250
cue_thickness = 4
cue_max_displacement = 100
# safe displacement is the length the cue stick can be pulled before
# causing the ball to move
cue_safe_displacement = 1
aiming_line_length = 14

# ball settings
total_ball_num = 16
ball_radius = 14
ball_mass = 14
ball_colors = [
    (255, 255, 255),
    (0, 200, 200),
    (0, 0, 200),
    (150, 0, 0),
    (200, 0, 200),
    (200, 0, 0),
    (50, 0, 0),
    (100, 0, 0),
    (0, 0, 0),
    (0, 200, 200),
    (0, 0, 200),
    (150, 0, 0),
    (200, 0, 200),
    (200, 0, 0),
    (50, 0, 0),
    (100, 0, 0)
]
ball_stripe_thickness = 2
# where the balls will be placed at the start
# relative to screen resolution
ball_starting_place_ratio = [0.75, 0.5]
white_ball_initial_pos = resolution * [0.25, 0.5]
ball_label_text_size = 10
forty_five_degree_cos = math.cos(math.radians(45))
array = np.array([[-hole_radius * 2, hole_radius], [-hole_radius, 0], [hole_radius, 0], [hole_radius * 2, hole_radius]])
middle_hole_offset = array
side_hole_offset = np.array([
    [- 2 * forty_five_degree_cos * hole_radius - hole_radius, hole_radius],
    [- forty_five_degree_cos * hole_radius, -
    forty_five_degree_cos * hole_radius],
    [forty_five_degree_cos * hole_radius,
     forty_five_degree_cos * hole_radius],
    [- hole_radius, 2 * forty_five_degree_cos * hole_radius + hole_radius]
])

# physics
# if the velocity of the ball is less then
# friction threshold then it is stopped
friction_threshold = 0.06
friction_coeff = 0.99

# menu
menu_text_color = (255, 255, 255)
menu_text_selected_color = (0, 0, 255)
menu_title_text = "Pool"
menu_buttons = ["Play Pool", "Exit"]
menu_margin = 20
menu_spacing = 10
menu_title_font_size = 40
menu_option_font_size = 20


# fonts need to be initialised before using


def get_default_font(size):
    font_defualt = pygame.font.get_default_font()
    return pygame.font.Font(font_defualt, size)
