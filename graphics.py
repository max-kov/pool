import pygame


class game_window():
    def __init__(self, vertical_size, horizontal_size, *args, **kwargs):
        pygame.init()
        pygame.display.set_caption("Gravity Simulator")

        self.surface = pygame.display.set_mode((vertical_size, horizontal_size), *args, **kwargs)
        self.size_x = vertical_size
        self.size_y = horizontal_size

        # fps control
        self.fps_clock = pygame.time.Clock()
        self.fps_limit = 60

    def update(self):
        pygame.display.update()

    def move_all_once(self, planets):
        for planet in planets:
            planet.move_once(self)
        self.update()
        self.fps_clock.tick(self.fps_limit)

    def main_menu(self):
        text_color = (255,255,255)
        text_selected_color = (0, 0, 255)
        font_name = pygame.font.get_default_font()
        title_font = pygame.font.Font(font_name,32)
        options_font = pygame.font.Font(font_name,20)

        title_text = "Gravity simulator"
        option_one_text = "Standart setup"
        option_two_text = "Fully random"
        option_three_text = "Load from file"

        title = title_font.render(title_text, False, text_color)
        option_one = options_font.render(option_one_text, False, text_color)
        option_two = options_font.render(option_two_text, False, text_color)
        option_three = options_font.render(option_three_text, False, text_color)

        title_selected = title_font.render(title_text, False, text_color)
        option_one_selected = options_font.render(option_one_text, False, text_selected_color)
        option_two_selected = options_font.render(option_two_text, False, text_selected_color)
        option_three_selected = options_font.render(option_three_text, False, text_selected_color)

        options = [[title,title_selected],
                   [option_one,option_one_selected],
                   [option_two,option_two_selected],
                   [option_three,option_three_selected]]

        option_size = [title_font.size(title_text),
                       options_font.size(option_one_text),
                       options_font.size(option_two_text),
                       options_font.size(option_three_text)]

        screen_mid = self.size_x/2
        margin = 20
        spacing = 10

        screen_y = (self.size_y - margin*2)/(len(options))
        text_place = []
        text_ending_place = []

        for num in range(0,len(options)):
            text_place.append((screen_mid-(option_size[num][0]/2),
                               num*screen_y+(option_size[num][1]/2)))
            text_ending_place.append((text_place[num][0]+option_size[num][0],
                                      text_place[num][1] + option_size[num][1]))

        for num in range(0,len(options)):
            self.surface.blit(options[num][0],text_place[num])

        for num in range(1,len(options)):
            pygame.draw.rect(self.surface, text_color, (text_place[num][0]-spacing, text_place[num][1]-spacing,
                                                        option_size[num][0]+spacing*2, option_size[num][1]+spacing*2),1)

        while 1:
            self.update()
            events = get_events()

            for num in range(0, len(options)):
                if events["mouse_pos"][0] in range(text_place[num][0]-spacing,text_ending_place[num][0]+spacing) and \
                    events["mouse_pos"][1] in range(text_place[num][1]-spacing, text_ending_place[num][1]+spacing):
                    if events["was_clicked"]:
                        self.surface.fill((0,0,0))
                        return num
                    else:
                        self.surface.blit(options[num][1],text_place[num])
                else:
                    self.surface.blit(options[num][0], text_place[num])

def get_events():
    was_closed = False
    was_clicked = False
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            was_closed = True
        elif event.type == pygame.KEYDOWN:
            was_closed = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            was_clicked = True

    return {"was_closed": was_closed,
            "was_clicked": was_clicked,
            "mouse_pos": mouse_pos}


def undraw(game_window, planet):
    pygame.draw.circle(game_window.surface, (0, 0, 0), (int(planet.x), int(planet.y)), int(planet.size))
