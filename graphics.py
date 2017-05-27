import numpy as np
import pygame

import config
import gamestate


class Canvas:
    def __init__(self):
        if config.fullscreen:
            config.set_max_resolution()
            self.surface = pygame.display.set_mode(config.resolution, pygame.FULLSCREEN)
        else:
            self.surface = pygame.display.set_mode(config.resolution)
        self.background = pygame.Surface(self.surface.get_size())
        self.background = self.background.convert()
        self.background.fill(config.table_color)
        self.surface.blit(self.background, (0, 0))


def add_separation_line(canvas):
    # white ball separation line
    pygame.draw.line(canvas.background, config.separation_line_color, (config.white_ball_initial_pos[0], 0),
                     (config.white_ball_initial_pos[0], config.resolution[1]))

def draw_main_menu(game_state):
    title_font = config.get_default_font(config.menu_title_font_size)
    options_font = config.get_default_font(config.menu_option_font_size)
    # calculating button sizes
    button_size = [options_font.size(label) for label in config.menu_buttons]
    # generating options buttons
    buttons = [
        # text when mouse is outside the button range
        [options_font.render(label, False, config.menu_text_color),
         # text when mouse is inside the button range
         options_font.render(label, False, config.menu_text_selected_color)]
        for label in config.menu_buttons]
    # generating the title
    title = [title_font.render(config.menu_title_text, False, config.menu_text_color),
             title_font.render(config.menu_title_text, False, config.menu_text_color)]

    buttons.insert(0, title)
    button_size.insert(0, title_font.size(config.menu_title_text))
    button_size = np.array(button_size)
    screen_mid = config.resolution[0] / 2
    change_in_y = (config.resolution[1] -
                   config.menu_margin * 2) / (len(buttons))
    screen_button_middles = np.stack((np.repeat([screen_mid], len(buttons)),
                                      np.arange(len(buttons)) * change_in_y), axis=1)

    text_starting_place = screen_button_middles + [-0.5, 0.5] * button_size
    text_ending_place = text_starting_place + button_size

    # writing text and drawing a rectangle around it
    for num in range(len(buttons)):
        game_state.canvas.surface.blit(
            buttons[num][0], text_starting_place[num])
        # no rectangle on the title
        if num > 0:
            pygame.draw.rect(game_state.canvas.surface, config.menu_text_color,
                             np.concatenate((text_starting_place[num] -
                                             config.menu_spacing, button_size[num] +
                                             config.menu_spacing * 2)), 1)

    button_clicked = 0
    # while a button was not clicked checks if mouse is in the button and if
    # so changes its colour
    while button_clicked == 0:
        pygame.display.update()
        user_events = gamestate.events()

        for num in range(1, len(buttons)):
            if np.all((np.less(text_starting_place[num] - config.menu_spacing, user_events["mouse_pos"]),
                       np.greater(text_ending_place[num] + config.menu_spacing, user_events["mouse_pos"]))):
                if user_events["clicked"]:
                    button_clicked = num
                else:
                    game_state.canvas.surface.blit(
                        buttons[num][1], text_starting_place[num])
            else:
                game_state.canvas.surface.blit(
                    buttons[num][0], text_starting_place[num])

    return button_clicked
