import pygame
import math
import physics

class Cue(pygame.sprite.Sprite):
    def __init__(self, target,hit_power=0.8):
        pygame.sprite.Sprite.__init__(self)

        self.visible = True

        self.target_ball = target

        self.hit_power = hit_power
        self.cue_length = 250
        self.cue_thickness = 3
        self.cue_color = (50, 50, 50)
        self.angle = 0
        self.max_displacement = 100
        self.displacement = self.target_ball.radius

        self.update()

    def update(self, *args):
        sprite_centre = self.cue_length + self.max_displacement

        self.image = pygame.Surface(
            (self.cue_length * 2 + 2 * self.max_displacement, self.cue_length * 2 + 2 * self.max_displacement))
        # color which will be ignored
        self.image.fill((200, 200, 200))
        self.image.set_colorkey((200, 200, 200))

        cos_a = math.cos(math.radians(self.angle))
        sin_a = math.sin(math.radians(self.angle))
        x_constant = cos_a * self.cue_thickness
        y_constant = sin_a * self.cue_thickness

        points = [
            (x_constant, -y_constant),
            (-x_constant, y_constant),
            (self.cue_length * sin_a - x_constant, self.cue_length * cos_a + y_constant),
            (self.cue_length * sin_a + x_constant, self.cue_length * cos_a - y_constant)
        ]

        shifted_point_list = [
            (a + sprite_centre + self.displacement * sin_a, b + sprite_centre + self.displacement * cos_a) for a, b in
            points]

        if self.visible:
            pygame.draw.polygon(self.image, self.cue_color, shifted_point_list)

        self.rect = self.image.get_rect()
        self.rect.center = self.target_ball.pos.tolist()

        self.points_on_screen = [
            (a + self.target_ball.pos[0] + self.displacement * sin_a, b + self.target_ball.pos[1] + self.displacement * cos_a) for
            a, b in points]

    def set_displacement(self, new_displacement):
        self.displacement = new_displacement

    def is_point_in_cue(self, point):
        # this algorithm splits up the rectangle into 4 triangles using the point provided
        # if the point provided is inside the triangle the sum of triangle areas should be equal to that of the rectangle

        # calculating rect sides
        rect_sides = [self.cue_thickness * 2, self.cue_length] * 2
        # calculating inside triangle sides
        triangle_sides = [physics.point_distance(rpoint, point) for rpoint in self.points_on_screen]
        triangle_areas = [physics.triangle_area(triangle_sides[side - 1], triangle_sides[side], rect_sides[side - 1])
                          for side in range(1, len(self.points_on_screen))]
        triangle_areas.append(physics.triangle_area(triangle_sides[3], triangle_sides[0], rect_sides[3]))
        inside_area = sum(triangle_areas)
        rect_area = rect_sides[0] * rect_sides[1]

        return (rect_area - inside_area + 4 >= 0)

    def update_cue_displacement(self, mouse_pos, initial_mouse_dist):
        displacement = physics.point_distance(mouse_pos, tuple(self.target_ball.pos)) - initial_mouse_dist + self.target_ball.radius
        if displacement > self.max_displacement:
            self.displacement = self.max_displacement
        elif displacement < self.target_ball.radius:
            self.displacement = self.target_ball.radius
        else:
            self.displacement = displacement

    def make_visible(self):
        self.visible = True

    def make_invisible(self):
        self.visible = False

    def check_if_clicked(self, game_state, initial_mouse_pos):
        def draw_lines(target_ball, angle, color):
            x,y = self.target_ball.pos
            dy = math.cos(math.radians(angle))
            dx = math.sin(math.radians(angle))

            line_length = 10

            while game_state.resolution[1]>y>0 and game_state.resolution[0] > x > 0:
                x+=line_length*dx
                y+=line_length*dy
                next_x = x + line_length * dx
                next_y = y + line_length * dy
                pygame.draw.line(game_state.canvas.surface,color,(x,y),(next_x,next_y))
                x=next_x
                y=next_y

        if self.is_point_in_cue(initial_mouse_pos):
            prev_angle = self.angle

            self.visible = 1

            initial_mouse_dist = physics.point_distance(initial_mouse_pos, tuple(self.target_ball.pos))
            game_state.mark_one_frame()
            pygame.event.get()

            # cue was displaced from the cue ball
            while pygame.mouse.get_pressed()[0]:
                pygame.event.get()
                final_pos = pygame.mouse.get_pos()
                dx = self.target_ball.pos[0] - final_pos[0]
                dy = self.target_ball.pos[1] - final_pos[1]

                self.update_cue_displacement(final_pos, initial_mouse_dist)

                prev_angle = self.angle
                if not dx == 0:
                    self.angle = 90 - math.degrees(math.atan(dy / dx))
                    if dx > 0:
                        self.angle -= 180

                game_state.all_sprites.clear(game_state.canvas.surface, game_state.canvas.background)
                game_state.all_sprites.draw(game_state.canvas.surface)
                game_state.all_sprites.update(game_state)
                draw_lines(self.target_ball, prev_angle + 180,game_state.table_color)
                draw_lines(self.target_ball, self.angle + 180,(255,255,255))
                pygame.display.flip()

                game_state.mark_one_frame()

            draw_lines(self.target_ball, self.angle + 180, game_state.table_color)

            disp_temp = self.displacement - self.target_ball.radius - 1
            if disp_temp > 0:
                if self.displacement > self.target_ball.radius:
                    for cur_disp in range(int(self.displacement), self.target_ball.radius, -1):
                        self.set_displacement(cur_disp)
                        game_state.redraw_all()
                        game_state.mark_one_frame()

                self.target_ball.add_force(-(disp_temp * math.sin(math.radians(self.angle))) * self.hit_power,
                                           -(disp_temp * math.cos(math.radians(self.angle))) * self.hit_power)

                self.make_invisible()
