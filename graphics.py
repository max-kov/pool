import pygame
import numpy as np


class Canvas:
    def __init__(self, vertical_size, horizontal_size, background_color, *args, **kwargs):
        self.surface = pygame.display.set_mode((vertical_size, horizontal_size), *args, **kwargs)
        self.size_x = vertical_size
        self.size_y = horizontal_size

        self.background = pygame.Surface(self.surface.get_size())
        self.background = self.background.convert()
        self.background.fill(background_color)

        self.surface.blit(self.background, (0, 0))

def draw_main_menu(game_state):
    def check_mouse_pos(text_starting_place, text_ending_place, spacing, button_num):
        mouse_pos = pygame.mouse.get_pos()
        return np.all((np.less(text_starting_place[button_num]-spacing,mouse_pos),
                       np.greater(text_ending_place[button_num]+spacing,mouse_pos)))

    text_color = (255, 255, 255)
    text_selected_color = (0, 0, 255)
    font_name = pygame.font.get_default_font()
    title_font = pygame.font.Font(font_name, 40)
    options_font = pygame.font.Font(font_name, 20)

    title_text = "Pool"
    menu_buttons = ["Play Pool", "Fully random", "Exit"]
    # generating options buttons
    buttons = [
        # text when mouse is outside the button range
        [options_font.render(label, False, text_color),
         # text when mouse is inside the button range
         options_font.render(label, False, text_selected_color)]
        for label in menu_buttons]
    # calculating button sizes
    button_size = [options_font.size(label) for label in menu_buttons]

    # generating the title
    title = [title_font.render(title_text, False, text_color),
             title_font.render(title_text, False, text_color)]
    buttons.insert(0, title)
    button_size.insert(0, title_font.size(title_text))
    button_size = np.array(button_size)

    margin = 20
    spacing = 10

    screen_mid = game_state.canvas.size_x / 2
    change_in_y = (game_state.canvas.size_y - margin * 2) / (len(buttons))

    screen_button_middles = np.stack((np.repeat([screen_mid],len(buttons)),
                                      np.arange(len(buttons))*change_in_y),axis=1)


    text_starting_place = screen_button_middles+[-0.5,0.5]*button_size
    text_ending_place = text_starting_place+button_size

    # writing text and drawing a rectangle around it
    for num in range(len(buttons)):
        game_state.canvas.surface.blit(buttons[num][0], text_starting_place[num])
        # no rectangle on the title
        if num > 0:
            pygame.draw.rect(game_state.canvas.surface, text_color,
                             np.concatenate((text_starting_place[num]-spacing,button_size[num]+spacing*2)),1)

    button_clicked = 0
    # while a button was not clicked checks if mouse is in the button and if so changes its colour
    while button_clicked==0:
        pygame.display.update()
        user_events = game_state.events()

        for num in range(1, len(buttons)):
            if check_mouse_pos(text_starting_place, text_ending_place, spacing, num):
                if user_events["clicked"]:
                    button_clicked = num
                else:
                    game_state.canvas.surface.blit(buttons[num][1], text_starting_place[num])
            else:
                game_state.canvas.surface.blit(buttons[num][0], text_starting_place[num])

    return button_clicked
