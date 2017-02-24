import pygame


class Canvas:
    def __init__(self, vertical_size, horizontal_size, *args, **kwargs):
        self.surface = pygame.display.set_mode((vertical_size, horizontal_size), *args, **kwargs)
        self.size_x = vertical_size
        self.size_y = horizontal_size

        # fps control
        self.fps_clock = pygame.time.Clock()
        self.fps_limit = 200

    # def update(self):
    #     pygame.display.update()

    def fps(self):
        return self.fps_clock.get_fps()

    def redraw_balls(self,balls):
        for ball in balls:
            # this doesnt move the ball anywhere, just resets it
            ball.move_to(ball.x,ball.y)
        self.update()

    # def move_all_once(self, balls):
    #     for ball in balls:
    #         ball.move_once()
    #     self.update()
    #     self.fps_clock.tick()

    def draw_main_menu(self,table_color):
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

        return text_starting_place, text_ending_place, spacing, buttons



    def draw_table_holes(self, gameState):
        for table_hole in gameState.table_holes:
            pygame.draw.circle(self.surface, (0, 0, 0), table_hole, int(gameState.hole_rad))

    def draw_table_sides(self,gameState):
        pygame.draw.rect(self.surface, gameState.side_color, (0, 0, self.size_x, gameState.table_margin))
        pygame.draw.rect(self.surface, gameState.side_color, (self.size_x - gameState.table_margin, 0, self.size_x, self.size_y))
        pygame.draw.rect(self.surface, gameState.side_color, (0, self.size_y - gameState.table_margin, self.size_x, self.size_y))
        pygame.draw.rect(self.surface, gameState.side_color, (0, 0, gameState.table_margin, self.size_y))


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
