import pygame


class game_window():
    def __init__(self, vertical_size, horizontal_size, *args, **kwargs):
        pygame.init()
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


def get_events():
    was_closed = False
    was_clicked = False
    mouse_pos = (0, 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            was_closed = True
        elif event.type == pygame.KEYDOWN:
            was_closed = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            was_clicked = True

    return {"was_closed": was_closed,
            "was_clicked": was_clicked,
            "mouse_pos": mouse_pos}


def undraw(game_window, planet):
    pygame.draw.circle(game_window.surface, (0, 0, 0), (int(planet.x), int(planet.y)), int(planet.size))
