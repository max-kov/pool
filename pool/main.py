import pygame

import collisiontests
import event
import gamestate
import graphics


was_quit = False
while not was_quit:
    game = gamestate.GameState()
    button_pressed = graphics.draw_main_menu(game)

    if button_pressed == 1:
        game.start_pool()
        events = event.events()
        was_quit = events["closed"]
        while not was_quit and not game.is_game_over:
            events = event.events()
            was_quit = events["closed"]
            collisiontests.resolve_all_collisions(game.balls, game.holes, game.table_sides)
            game.redraw_all()

            if game.all_not_moving():
                game.check_pool_rules()
                game.cue.make_visible(game.current_player)
                while game.all_not_moving() and not was_quit and not game.is_game_over:
                    game.redraw_all()
                    events = event.events()
                    if game.cue.is_clicked(events):
                        game.cue.cue_is_active(game, events)
                    elif game.can_move_white_ball and game.white_ball.is_clicked(events):
                        game.white_ball.is_active(game, game.is_behind_line_break())

    if button_pressed == 2:
        was_quit = True
pygame.quit()
