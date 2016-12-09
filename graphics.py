import pygame


class GameWindow:
    def __init__(self, vertical_size, horizontal_size, *args, **kwargs):
        self.surface = pygame.display.set_mode((vertical_size, horizontal_size), *args, **kwargs)
        self.size_x = vertical_size
        self.size_y = horizontal_size

        # fps control
        self.fps_clock = pygame.time.Clock()
        self.fps_limit = 200

    def update(self):
        pygame.display.update()

    def fps(self):
        return self.fps_clock.get_fps()

    def move_all_once(self, planets):
        for planet in planets:
            planet.move_once()
        self.update()
        self.fps_clock.tick()

    def main_menu(self):
        def check_mouse_pos(text_starting_place, text_ending_place, spacing, button_num):
            mouse_pos = pygame.mouse.get_pos()
            if (text_starting_place[button_num][0] - spacing < mouse_pos[0] < text_ending_place[button_num][
                0] + spacing) and \
                    (text_starting_place[button_num][1] - spacing < mouse_pos[1] < text_ending_place[button_num][
                        1] + spacing):
                return True
            else:
                return False

        text_color = (255, 255, 255)
        text_selected_color = (0, 0, 255)
        font_name = pygame.font.get_default_font()
        title_font = pygame.font.Font(font_name, 40)
        options_font = pygame.font.Font(font_name, 20)

        title_text = "Gravity Simulator"
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

        screen_mid = self.size_x / 2
        margin = 20
        spacing = 10

        screen_y = (self.size_y - margin * 2) / (len(buttons))

        # generating text coordinates
        text_starting_place = [(screen_mid - (button_size[num][0] / 2),
                                num * screen_y + (button_size[num][1] / 2)) for num in range(len(buttons))]
        text_ending_place = [(text_starting_place[num][0] + button_size[num][0],
                              text_starting_place[num][1] + button_size[num][1]) for num in range(len(buttons))]

        # writing text and drawing a rectangle around it
        for num in range(len(buttons)):
            self.surface.blit(buttons[num][0], text_starting_place[num])
            # no rectangle on the title
            if num > 0:
                pygame.draw.rect(self.surface, text_color,
                                 (text_starting_place[num][0] - spacing, text_starting_place[num][1] - spacing,
                                  button_size[num][0] + spacing * 2, button_size[num][1] + spacing * 2), 1)

        was_clicked = False
        button_clicked = 0

        while not was_clicked:
            self.update()
            user_events = events()

            for num in range(1, len(buttons)):
                if check_mouse_pos(text_starting_place, text_ending_place, spacing, num):
                    if user_events["clicked"]:
                        was_clicked = True
                        button_clicked = num
                    else:
                        self.surface.blit(buttons[num][1], text_starting_place[num])
                else:
                    self.surface.blit(buttons[num][0], text_starting_place[num])

        self.surface.fill((0, 100, 0))
        return button_clicked


def events():
    closed = False
    clicked = False
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type in [pygame.QUIT, pygame.KEYDOWN]:
            closed = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True

    return {"closed": closed,
            "clicked": clicked,
            "mouse_pos": mouse_pos}


def undraw(game_window, planet):
    pygame.draw.circle(game_window.surface, (0, 0, 0), (int(planet.x), int(planet.y)), int(planet.size))
