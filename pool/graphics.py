import numpy as np
import pygame

import config
import event


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


def create_buttons(text, text_font, text_color_normal, text_color_on_hover):
    # this function generates button objects using button text, button font, normal colour and color of the text when
    # the mouse is hovering over the button

    button_size = np.array([text_font[num].size(text[num]) for num in range(len(text))])
    # generating button objects
    buttons = [
        # text when mouse is outside the button range
        [text_font[num].render(text[num], False, text_color_normal[num]),
         # text when mouse is inside the button range
         text_font[num].render(text[num], False, text_color_on_hover[num])]
        for num in range(len(text))]

    screen_mid = config.resolution[0] / 2
    change_in_y = (config.resolution[1] -
                   config.menu_margin * 2) / (len(buttons))
    screen_button_middles = np.stack((np.repeat([screen_mid], len(buttons)),
                                      np.arange(len(buttons)) * change_in_y), axis=1)

    text_starting_place = screen_button_middles + [-0.5, 0.5] * button_size
    text_ending_place = text_starting_place + button_size

    return buttons, button_size, text_starting_place, text_ending_place


def draw_main_menu(game_state):
    buttons, button_size, text_starting_place, text_ending_place = create_buttons(
        [config.menu_title_text] + config.menu_buttons,
        [config.get_default_font(config.menu_title_font_size)] + [
            config.get_default_font(config.menu_option_font_size)] * 3,
        [config.menu_text_color] * 4,
        [config.menu_text_color] + [config.menu_text_selected_color] * 3)
    draw_rects(button_size, buttons, game_state, text_starting_place, emit=[0])
    button_clicked = iterate_until_button_press(buttons, game_state, text_ending_place,
                                                text_starting_place)

    return button_clicked


def iterate_until_button_press(buttons, game_state, text_ending_place, text_starting_place):
    # while a button was not clicked this method checks if mouse is in the button and if it is
    # changes its colour
    button_clicked = 0
    while button_clicked == 0:
        pygame.display.update()
        user_events = event.events()
        # the first button is the title which is unclickable, thus iterating from 1 to len(buttons)
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
        if user_events["closed"] or user_events["quit_to_main_menu"]:
            button_clicked = len(buttons)-1
    return button_clicked


def draw_rects(button_size, buttons, game_state, text_starting_place, emit=list()):
    # drawing a rectangle around the button text
    for num in range(len(buttons)):
        game_state.canvas.surface.blit(
            buttons[num][0], text_starting_place[num])
        # emit contains indexes of buttons which do not need a rectangle around them
        if not num in emit:
            pygame.draw.rect(game_state.canvas.surface, config.menu_text_color,
                             np.concatenate((text_starting_place[num] -
                                             config.menu_spacing, button_size[num] +
                                             config.menu_spacing * 2)), 1)
