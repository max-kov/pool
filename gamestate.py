import itertools
import math

import numpy as np
import pygame

import ball
import config
import cue
import graphics
import table_sprites


class GameState:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(config.window_caption)
        self.canvas = graphics.Canvas()
        self.fps_clock = pygame.time.Clock()

    def fps(self):
        return self.fps_clock.fps()

    def mark_one_frame(self):
        self.fps_clock.tick(config.fps_limit)

    def create_balls(self):
        for i in range(config.total_ball_num):
            self.balls.add(ball.Ball(i))

    def set_pool_balls(self):
        coord_shift = np.array([math.sin(math.radians(60)) * config.ball_radius *
                                2, -config.ball_radius])
        counter = [0, 0]
        initial_place = config.ball_starting_place_ratio * config.resolution
        for ball in self.balls:
            if not ball.number == 0:
                ball.move_to(initial_place + coord_shift * counter, do_update=True)
                if counter[1] == counter[0]:
                    counter[0] += 1
                    counter[1] = -counter[0]
                else:
                    counter[1] += 2
            else:
                ball.move_to(config.white_ball_initial_pos, do_update=True)
                self.white_ball = ball
        self.all_sprites.add(self.balls)

    def start_pool(self):
        # game state variables
        # game always starts with p1, so odd numbers are player1 turns
        self.turn_number = 0
        self.stripes_decided = False
        self.player1_stripes = False
        self.can_move_white_ball = True
        self.stripes_remaining = True
        self.solids_remaining = True
        self.player1_pots_8ball = False
        self.player2_pots_8ball = False
        # drawing the table
        self.generate_table()
        graphics.add_separation_line(self.canvas)
        self.create_balls()
        self.set_pool_balls()
        self.cue = cue.Cue(self.white_ball)
        self.all_sprites.add(self.cue)

    def is_behind_line_break(self):
        # 1st break should be made from behind the separation line on the table
        return self.turn_number == 1

    def redraw_all(self, update=True):
        self.all_sprites.clear(self.canvas.surface, self.canvas.background)
        self.all_sprites.draw(self.canvas.surface)
        self.all_sprites.update(self)
        if update:
            pygame.display.flip()
        self.mark_one_frame()

    def all_not_moving(self):
        return_value = True
        for ball in self.balls:
            if np.count_nonzero(ball.velocity) > 0:
                return_value = False
                break
        return return_value

    def generate_table(self):
        self.white_ball_1st_hit_is_set = False
        self.white_ball_1st_hit_is_stripes = False
        self.potted = []
        self.balls = pygame.sprite.Group()
        self.holes = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.OrderedUpdates()
        # stores the invisible table lines which reflect the ball when it
        # touches the table side
        self.table_sides = []
        table_side_points = np.empty((1, 2))
        # holes_x and holes_y holds the possible xs and ys table holes
        # with a position ID in the second tuple field
        # so the top left hole has id 1,1
        holes_x = [(config.table_margin, 1), (config.resolution[0] /
                                              2, 2), (config.resolution[0] - config.table_margin, 3)]
        holes_y = [(config.table_margin, 1),
                   (config.resolution[1] - config.table_margin, 2)]
        # next three lines are a hack to make and arrange the hole coordinates
        # in the correct sequence
        all_hole_positions = np.array(
            list(itertools.product(holes_y, holes_x)))
        all_hole_positions = np.fliplr(all_hole_positions)
        all_hole_positions = np.vstack(
            (all_hole_positions[:3], np.flipud(all_hole_positions[3:])))
        for hole_pos in all_hole_positions:
            self.holes.add(table_sprites.Hole(hole_pos[0][0], hole_pos[1][0]))
            # this will generate the diagonal, vertical and horizontal table
            # pieces which will reflect the ball when it hits the table sides
            # they are generated using 4x2 offset matrices (4 points around the hole)
            # with the first point of the matrix is the starting point and the
            # last point is the ending point, these 4x2 matrices are
            # concatenated together
            # also the martices must be flipped using numpy.flipud()
            # after reflecting them using 2x1 reflection matrices, otherwise
            # starting and ending points would be reversed
            if hole_pos[0][1] == 2:
                # hole_pos[0,1]=2 means x coordinate ID is 2 which means this
                # hole is in the middle
                offset = config.middle_hole_offset
            else:
                offset = config.side_hole_offset
            if hole_pos[1][1] == 2:
                offset = np.flipud(offset) * [1, -1]
            if hole_pos[0][1] == 1:
                offset = np.flipud(offset) * [-1, 1]
            table_side_points = np.append(
                table_side_points, [hole_pos[0][0], hole_pos[1][0]] + offset, axis=0)
        # deletes the 1st point in array (leftover form np.empty)
        table_side_points = np.delete(table_side_points, 0, 0)
        for num, point in enumerate(table_side_points[:-1]):
            # this will skip lines inside the circle
            if num % 4 != 1:
                self.table_sides.append(table_sprites.TableSide(
                    [point, table_side_points[num + 1]]))
        self.table_sides.append(table_sprites.TableSide(
            [table_side_points[-1], table_side_points[0]]))
        self.table_coloring = table_sprites.TableColoring(
            config.resolution, config.table_side_color, table_side_points)
        self.all_sprites.add(self.table_coloring)
        self.all_sprites.add(self.holes)

    def game_over(self, p1_won):
        # when the game is over a message is displayed
        font = config.get_default_font(config.game_over_label_font_size)
        if p1_won:
            text = "PLAYER 1 WON!"
        else:
            text = "PLAYER 2 WON!"
        rendered_text = font.render(text, False, (255, 255, 255))
        self.canvas.surface.blit(rendered_text, (config.resolution - font.size(text)) / 2)
        pygame.display.flip()
        while not (events()["closed"] or events()["clicked"]):
            pass


    def turn_over(self):
        self.turn_number += 1

    def free_hit(self):
        self.can_move_white_ball = True

    def is_1st_players_turn(self):
        return self.turn_number % 2 == 0

    def check_potted(self):
        self.can_move_white_ball = False
        # if white ball is potted, it will be created again and placed in the middle
        if 0 in self.potted:
            new_white_ball = ball.Ball(0)
            new_white_ball.move_to(config.white_ball_initial_pos, do_update=True)
            self.white_ball = new_white_ball
            self.cue.target_ball = new_white_ball
            self.balls.add(new_white_ball)
            self.all_sprites.add(self.white_ball)
            self.potted.remove(0)
            self.free_hit()
        if 8 in self.potted:
            if (self.is_1st_players_turn() and self.player1_pots_8ball) or \
                    (not self.is_1st_players_turn() and self.player2_pots_8ball):
                self.game_over(self.is_1st_players_turn())
            else:
                self.game_over(not self.is_1st_players_turn())
            self.potted.remove(8)

    def check_remaining(self):
        # a check if all striped or solid balls were potted
        stripes_remaining = False
        solids_remaining = False
        for remaining_ball in self.balls:
            if remaining_ball.number != 0 or remaining_ball.number != 8:
                stripes_remaining = stripes_remaining or remaining_ball.is_striped
                solids_remaining = solids_remaining or not remaining_ball.is_striped
        self.stripes_remaining = stripes_remaining
        self.solids_remaining = solids_remaining

        # decides if on of the players (or both) should be potting 8ball
        if not self.stripes_remaining or not self.solids_remaining:
            if not self.stripes_remaining:
                if self.player1_stripes:
                    self.player1_pots_8ball = True
                else:
                    self.player2_pots_8ball = True
            # both player can have the 8 ball as a target at the same time
            if not self.solids_remaining:
                if not self.player1_stripes:
                    self.player1_pots_8ball = True
                else:
                    self.player2_pots_8ball = True

    def first_collision(self, ball_combination):
        self.white_ball_1st_hit_is_set = True
        self.white_ball_1st_hit_8ball = ball_combination[0].number == 8 or ball_combination[1].number == 8
        if ball_combination[0].number == 0:
            self.white_ball_1st_hit_is_stripes = ball_combination[1].is_striped
        else:
            self.white_ball_1st_hit_is_stripes = ball_combination[0].is_striped

    def check_pool_rules(self):
        turn_over = False
        free_hit = False

        # checks if the 1st white ball hit is the same as the players target ball type
        # for example if the first white hit of the white ball is a striped ball,
        # but the player hits a solid ball, it is next players turn and he can move the white ball
        if not self.white_ball_1st_hit_is_set:
            free_hit = True
            turn_over = True
        else:
            if self.stripes_decided and not self.white_ball_1st_hit_8ball:
                if self.is_1st_players_turn():
                    if not ((self.player1_stripes and self.white_ball_1st_hit_is_stripes) or
                                (not self.player1_stripes and not self.white_ball_1st_hit_is_stripes)):
                        free_hit = True
                        turn_over = True
                else:
                    if not ((not self.player1_stripes and self.white_ball_1st_hit_is_stripes) or
                                (self.player1_stripes and not self.white_ball_1st_hit_is_stripes)):
                        free_hit = True
                        turn_over = True

            # checks if the 8ball was the first ball hit, and if so checks if the player needs to pot the 8ball
            # and if not he gets penalised
            if self.white_ball_1st_hit_8ball:
                if not ((self.is_1st_players_turn() and self.player1_pots_8ball) or
                            (not self.is_1st_players_turn() and self.player2_pots_8ball)):
                    free_hit = True
                    turn_over = True

        # if it wasnt decided which player goes for which type of balls
        # and the player potted the balls exclusively of one color (excluting white balls)
        # then it is decided based on which players turn it is right now and which type
        # of balls he potted
        if not self.stripes_decided and len(self.potted) > 0:
            if np.all(np.array(self.potted) > 8):
                # all balls potted were stripes
                self.player1_stripes = self.is_1st_players_turn()
                self.stripes_decided = True
            elif np.all(np.array(self.potted) < 8):
                # all balls potted were solids
                self.player1_stripes = not self.is_1st_players_turn()
                self.stripes_decided = True

        # checks which balls were potted
        only_stripes_potted = True
        only_solids_potted = True
        for potted_ball in self.potted:
            only_solids_potted = only_solids_potted and (potted_ball < 8)
            only_stripes_potted = only_stripes_potted and (potted_ball > 8)

        # checks if the player potted any wrong ball types
        #if he pots a solid ball when he needs to pot striped balls, it is next players turn
        if self.stripes_decided and len(self.potted) > 0 and (only_stripes_potted or only_solids_potted):
            if self.is_1st_players_turn():
                if not ((self.player1_stripes and only_stripes_potted) or
                            (not self.player1_stripes and only_solids_potted)):
                    turn_over = True
            else:
                if not ((not self.player1_stripes and only_stripes_potted) or
                            (self.player1_stripes and only_solids_potted)):
                    turn_over = True
        else:
            turn_over = True

        if free_hit:
            self.free_hit()
        if turn_over:
            self.turn_over()
        self.white_ball_1st_hit_is_set = False
        self.potted = []

def events():
    closed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            closed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                closed = True

    return {"closed": closed,
            "clicked": pygame.mouse.get_pressed()[0],
            "mouse_pos": np.array(pygame.mouse.get_pos())}
